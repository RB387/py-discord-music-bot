from dataclasses import dataclass
from typing import Dict

import discord
from discord import FFmpegOpusAudio
from yt_dlp import YoutubeDL

from lib.core.injector import ClientProtocol, FileConstructable
from lib.players.protocol import AudioMeta, PlayerProtocol


@dataclass
class StreamPlayer(PlayerProtocol, FileConstructable):
    ydl_opts: Dict[str, str]
    ffmpeg_opts: Dict[str, str]

    @classmethod
    def __from_config__(
        cls, config: Dict[str, Dict], **_: Dict[str, ClientProtocol]
    ) -> ClientProtocol:
        ydl_opts = config.get('ydl', {})
        ffmpeg_opts = config.get('ffmpeg', {})

        return cls(
            ydl_opts=ydl_opts,
            ffmpeg_opts=ffmpeg_opts,
        )

    async def get_audio(self, meta: AudioMeta) -> FFmpegOpusAudio:
        return await discord.FFmpegOpusAudio.from_probe(meta.url, **self.ffmpeg_opts)

    async def get_info(self, url: str) -> AudioMeta:
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(str(url), download=False)
            video_info = _find_video_info(info)

            return AudioMeta(
                author=info.get('uploader', 'Unknown'),
                url=video_info['url'],
                name=info['title'],
                original_url=url,
            )


def _find_video_info(info: dict) -> dict:
    for video_format in info['formats']:
        if video_format.get('audio_ext', 'none') != 'none':
            return video_format

    raise ValueError('No audio format found')
