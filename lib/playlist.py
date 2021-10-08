import inspect
from asyncio import Lock
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    TypeVar,
    Union,
    cast,
)

from discord.ext.commands import Context

from lib.core.bot import DiscordBot
from lib.core.injector import ClientProtocol
from lib.core.logger import Logger
from lib.messenger import Message, Messenger
from lib.players.compose import ComposePlayer
from lib.players.protocol import AudioMeta
from lib.utils.voice import (
    get_voice_channel_id,
    get_voice_client,
    wait_play,
)

T = TypeVar('T')


def _playlist_factory():
    return defaultdict(list)


@dataclass
class Playlist(ClientProtocol):
    player: ComposePlayer
    logger: Logger
    bot: DiscordBot
    messenger: Messenger
    _lock: Lock = field(init=False, default_factory=Lock)
    _playlist: Dict[int, List[AudioMeta]] = field(init=False, default_factory=_playlist_factory)

    async def clear(self, channel_id: int):
        async with self._lock:
            qname = self._get_queue_name(channel_id)
            playlist = self._playlist.get(channel_id, [])

            if len(playlist) > 1:
                self._playlist[channel_id] = [playlist[0]]

            self.bot.clear_queue(qname)

    async def add(self, ctx: Context, url: str) -> AudioMeta:
        voice = await get_voice_client(ctx, self.bot)
        channel_id = get_voice_channel_id(ctx)
        meta = await self.player.get_info(url)

        async def _play():
            try:
                audio = await self.player.get_audio(meta)
                await wait_play(voice, audio)
            except Exception as exc:
                self.logger.exception('Failed to play audio')
                msg = Message(
                    template_name='error',
                    args=(f'play `{meta.name}`', exc.__class__.__name__),
                )
                await self.messenger.send(
                    ctx=ctx,
                    title='Error',
                    msgs=[msg],
                )
            finally:
                async with self._lock:
                    self._playlist[channel_id].pop(0)

        async with self._lock:
            qname = self._get_queue_name(channel_id)
            await self.bot.queue_task(qname, _play)
            self._playlist[channel_id].append(meta)

        return meta

    async def skip(self, ctx: Context):
        voice = await get_voice_client(ctx, self.bot)
        voice.stop()

    async def pause(self, ctx: Context):
        voice = await get_voice_client(ctx, self.bot)
        voice.pause()

    async def resume(self, ctx: Context):
        voice = await get_voice_client(ctx, self.bot)
        voice.resume()

    def list(self, channel_id: int) -> Iterable[AudioMeta]:
        return tuple(self._playlist[channel_id])

    def size(self, channel_id: int) -> int:
        qname = self._get_queue_name(channel_id)
        return self.bot.qsize(qname)

    @staticmethod
    async def channel_from_context(ctx: Context, fn: Callable[[int], Union[T, Awaitable[T]]]) -> T:
        channel_id = get_voice_channel_id(ctx)

        res = fn(channel_id)
        if inspect.isawaitable(res):
            res = cast(Awaitable[T], res)
            return await res

        res = cast(T, res)
        return res

    @staticmethod
    def _get_queue_name(channel_id: int) -> str:
        return f'playlist:{channel_id}'
