from dataclasses import dataclass
from typing import Dict

from discord.ext.commands import Context

from lib.core import (
    ClientProtocol,
    DiscordBot,
    FileConstructable,
    router,
)
from lib.emoji import Emoji
from lib.messenger import Message, Messenger
from lib.playlist import Playlist
from lib.utils.voice import NotConnectedToVoiceChannel


@router.command('play')
@dataclass
class Player(FileConstructable):
    messages_ttl: int
    playlist: Playlist

    bot: DiscordBot
    messenger: Messenger

    @classmethod
    def from_config(cls, config: Dict[str, Dict], **clients) -> ClientProtocol:
        messages_ttl = int(config['common']['messages_ttl'])

        return cls(messages_ttl=messages_ttl, **clients)

    async def handle(self, ctx: Context, *args: str):
        url_or_name = ' '.join(args)
        async with ctx.typing():
            try:
                meta = await self.playlist.add(ctx, url_or_name)
            except NotConnectedToVoiceChannel:
                msg = Message(template_name='not-connected')
                return await self.messenger.send(
                    ctx=ctx,
                    title='Error',
                    msgs=[msg],
                    delete_after=self.messages_ttl,
                )

            msg = Message(template_name='play-song', args=(meta.name, self.playlist.size))
            await self.messenger.react(ctx, Emoji.OK_HAND)
            await self.messenger.send(
                ctx=ctx,
                title='Play',
                msgs=[msg],
                delete_after=self.messages_ttl,
            )
