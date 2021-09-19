from asyncio import Lock
from dataclasses import dataclass, field
from typing import (
    Dict,
    Iterable,
    List,
)

from discord.ext.commands import Context

from lib.core.bot import DiscordBot
from lib.core.injector import ClientProtocol, FileConstructable
from lib.core.logger import Logger
from lib.messenger import Message, Messenger
from lib.players.compose import ComposePlayer
from lib.players.protocol import AudioMeta
from lib.utils.voice import get_voice_client, wait_play


@dataclass
class Playlist(FileConstructable):
    player: ComposePlayer
    logger: Logger
    bot: DiscordBot
    messenger: Messenger
    playlist_queue: str
    _lock: Lock = field(init=False, default_factory=Lock)
    _playlist: List[AudioMeta] = field(init=False, default_factory=list)

    @classmethod
    def from_config(cls, config: Dict[str, Dict], **clients) -> ClientProtocol:
        playlist_queue = config['common']['playlist_queue']

        return cls(playlist_queue=playlist_queue, **clients)

    async def clear(self):
        await self.bot.clear_queue(self.playlist_queue)

    async def add(self, ctx: Context, url: str) -> AudioMeta:
        voice = await get_voice_client(ctx, self.bot)
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
                    self._playlist.pop(0)

        async with self._lock:
            await self.bot.add_task(self.playlist_queue, _play)
            self._playlist.append(meta)

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

    @property
    def list(self) -> Iterable[AudioMeta]:
        return tuple(self._playlist)

    @property
    def size(self) -> int:
        return self.bot.qsize(self.playlist_queue)
