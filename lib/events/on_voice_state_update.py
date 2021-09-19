from dataclasses import dataclass

from discord import (
    Guild,
    Member,
    VoiceClient,
    VoiceState,
)

from lib.core import ClientProtocol, router


@router.event('on_voice_state_update')
@dataclass
class OnVoiceUpdateHandler(ClientProtocol):
    @staticmethod
    async def handle(member: Member, _: VoiceState, __: VoiceState):
        guild: Guild = member.guild

        voice: VoiceClient = guild.voice_client
        if voice is None:
            # bot is not connected to voice channel
            return

        if len(voice.channel.members) == 1:
            # only bot left
            await voice.disconnect()
