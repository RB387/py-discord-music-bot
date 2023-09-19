from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.emoji import Emoji
from lib.messenger import Message, Messenger
from lib.playlist import Playlist


@router.command('loop')
@dataclass
class LoopQueue(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context, *args):
        """ Loop player queue """
        looped = await self.playlist.channel_from_context(ctx, self.playlist.loop)
        await self.messenger.react(ctx, Emoji.OK_HAND)

        template = 'loop-enabled' if looped else 'loop-disabled'
        await self.messenger.send(
            ctx=ctx,
            title='Loop',
            msgs=[Message(template)],
        )
