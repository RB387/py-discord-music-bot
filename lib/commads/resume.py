from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.emoji import Emoji
from lib.messenger import Messenger
from lib.playlist import Playlist


@router.command('resume')
@dataclass
class Resume(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context, *args):
        """ Resume song """
        await self.messenger.react(ctx, Emoji.RESUME)
        await self.playlist.resume(ctx)
