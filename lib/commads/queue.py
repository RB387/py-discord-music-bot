from dataclasses import dataclass

from discord.ext.commands import Context

from lib.core import ClientProtocol, router
from lib.messenger import Message, Messenger
from lib.playlist import Playlist
from lib.utils.voice import NotConnectedToVoiceChannel


@router.command('queue')
@dataclass
class QueueStatus(ClientProtocol):
    playlist: Playlist
    messenger: Messenger

    async def handle(self, ctx: Context):
        """ Get current player queue """
        try:
            playlist = await self.get_playlist(ctx)
        except NotConnectedToVoiceChannel:
            msg = Message(template_name='not-connected')
            return await self.messenger.send(
                ctx=ctx,
                title='Error',
                msgs=[msg],
            )

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

    async def get_playlist(self, ctx: Context):
        return await self.playlist.channel_from_context(ctx, self.playlist.list)
