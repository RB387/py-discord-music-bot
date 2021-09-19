from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.emoji import Emoji
from lib.messenger import Messenger
from lib.playlist import Playlist


@router.command('clear')
@dataclass
class PlaylistCleaner(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context):
        await self.messenger.react(ctx, Emoji.OK_HAND)
        await self.playlist.clear()
