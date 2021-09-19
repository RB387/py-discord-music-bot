from dataclasses import dataclass
from typing import Protocol

from discord import FFmpegOpusAudio


@dataclass(frozen=True)
class AudioMeta:
    original_url: str
    name: str
    author: str
    url: str


class PlayerProtocol(Protocol):
    async def get_audio(self, meta: AudioMeta) -> FFmpegOpusAudio:
        ...

    async def get_info(self, url: str) -> AudioMeta:
        ...
