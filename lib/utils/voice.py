from asyncio import Lock
from typing import Optional

from discord import (
    FFmpegOpusAudio,
    Guild,
    VoiceChannel,
    VoiceClient,
    VoiceState,
)
from discord.ext.commands import Context
from discord.utils import get

from lib.core.bot import DiscordBot


class NotConnectedToVoiceChannel(Exception):
    ...


def get_voice_channel_id(ctx: Context):
    author_voice: VoiceState = ctx.author.voice
    if author_voice is None:
        raise NotConnectedToVoiceChannel

    channel: VoiceChannel = author_voice.channel
    return channel.id


async def get_voice_client(ctx: Context, bot: DiscordBot) -> VoiceClient:
    guild: Guild = ctx.guild

    author_voice: VoiceState = ctx.author.voice
    if author_voice is None:
        raise NotConnectedToVoiceChannel

    channel: VoiceChannel = author_voice.channel
    client: VoiceClient = get(bot.voice_clients, guild=guild)

    if not client:
        await channel.connect()
        return get(bot.voice_clients, guild=guild)

    return client


async def wait_play(voice: VoiceClient, audio: FFmpegOpusAudio):
    lock = Lock()

    def _after(exc: Optional[Exception]):
        lock.release()

        if exc:
            raise exc

    await lock.acquire()
    voice.play(audio, after=_after)

    await lock.acquire()
