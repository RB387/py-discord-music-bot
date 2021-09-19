import discord
from discord import FFmpegOpusAudio
from youtube_dl import YoutubeDL

from lib.players.protocol import AudioMeta
from lib.players.stream import StreamPlayer


class YoutubeSearchPlayer(StreamPlayer):
    async def get_audio(self, meta: AudioMeta) -> FFmpegOpusAudio:
        return await discord.FFmpegOpusAudio.from_probe(meta.url, **self.ffmpeg_opts)

    async def get_info(self, url: str) -> AudioMeta:
        """ in this case url is video name """
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(str(url), download=False)
            video_info = info['entries'][0]

            return AudioMeta(
                author=video_info['channel'],
                url=video_info['url'],
                name=video_info['title'],
                original_url=url,
            )
