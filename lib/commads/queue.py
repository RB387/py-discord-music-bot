from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.messenger import Message, Messenger
from lib.playlist import Playlist


@router.command('queue')
@dataclass
class QueueStatus(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context):
        playlist = await self.get_playlist()
        msgs = []

        for idx, meta in enumerate(playlist):
            if idx == 0:
                msgs.append(Message(template_name='playing-now', args=(meta.name, meta.author)))
            else:
                msg = Message(template_name='queue-entry', args=(str(idx), meta.name, meta.author))
                msgs.append(msg)

        await self.messenger.send(
            ctx=ctx,
            title='Queue',
            msgs=msgs,
            delete_after=None,
        )

    async def get_playlist(self):
        return self.playlist.list
