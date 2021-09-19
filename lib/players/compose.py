import re
from dataclasses import dataclass

from discord import FFmpegOpusAudio

from lib.core.injector import ClientProtocol
from lib.players.protocol import AudioMeta, PlayerProtocol
from lib.players.stream import StreamPlayer
from lib.players.yt_search import YoutubeSearchPlayer

URL_REGEXP = re.compile(r'(http://|https://).*')


@dataclass
class ComposePlayer(PlayerProtocol, ClientProtocol):
    stream_player: StreamPlayer
    yt_search: YoutubeSearchPlayer

    async def get_info(self, url: str) -> AudioMeta:
        player = self.select_player(url)
        return await player.get_info(url)

    async def get_audio(self, meta: AudioMeta) -> FFmpegOpusAudio:
        player = self.select_player(meta.original_url)
        return await player.get_audio(meta)

    def select_player(self, url: str) -> PlayerProtocol:
        if not URL_REGEXP.match(url):
            return self.yt_search

        return self.stream_player
