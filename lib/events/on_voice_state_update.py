from dataclasses import dataclass

from discord import (
    Guild,
    Member,
    VoiceClient,
    VoiceState,
)

from lib.core import ClientProtocol, router
from lib.playlist import Playlist


@router.event('on_voice_state_update')
@dataclass
class OnVoiceUpdateHandler(ClientProtocol):
    playlist: Playlist

    async def handle(self, member: Member, _: VoiceState, __: VoiceState):
        guild: Guild = member.guild

        voice: VoiceClient = guild.voice_client
        if voice is None:
            # bot is not connected to voice channel
            return

        if len(voice.channel.voice_states) == 1:
            # voice states, because some members can be incognito
            # only bot left
            await self.playlist.clear(voice.channel.id)
            await voice.disconnect()
