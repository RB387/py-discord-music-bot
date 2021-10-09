from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.emoji import Emoji
from lib.messenger import Messenger
from lib.playlist import Playlist


@router.command('pause')
@dataclass
class Pause(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context):
        """ Pause current song """
        await self.messenger.react(ctx, Emoji.PAUSE)
        await self.playlist.pause(ctx)
