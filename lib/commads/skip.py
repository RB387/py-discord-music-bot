from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.emoji import Emoji
from lib.messenger import Messenger
from lib.playlist import Playlist


@router.command('skip')
@dataclass
class Skip(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context, *args):
        """ Skip current song """
        await self.messenger.react(ctx, Emoji.SKIP)
        await self.playlist.skip(ctx)
