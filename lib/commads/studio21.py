from dataclasses import dataclass
from typing import List

import aiohttp
from discord.ext.commands import Context

from lib.commads.play import Player
from lib.commads.queue import QueueStatus
from lib.core import ClientProtocol, router
from lib.players.protocol import AudioMeta

STUDIO_21_URL = 'http://icecast-studio21.cdnvideo.ru/S21_1'
_HEADERS = {
    'Host': 'studio21.ru',
    'Accept-Language': 'en-RU;q=1.0, ru-RU;q=0.9, uk-UA;q=0.8, de-DE;q=0.7, hi-RU;q=0.6',
    'Accept': '*/*',
    'User-Agent': 'PyDiscordMusicBot',
}


@router.command('21queue')
class Studio21QueueStatus(QueueStatus):
    async def get_playlist(self):
        meta = []

        async with aiohttp.ClientSession(headers=_HEADERS) as session:
            response = await session.get('https://studio21.ru/radio/ct')
            current_audio = await response.json()

            response = await session.get('https://studio21.ru/radio/lt')
            audios: List = await response.json()
            audios.insert(0, current_audio)

            for audio in audios:
                meta.append(
                    AudioMeta(
                        original_url=STUDIO_21_URL,
                        name=audio['t'],
                        author=audio['a'],
                        url=STUDIO_21_URL,
                    )
                )

        return meta


@router.command('studio21')
@dataclass
class Studio21Player(ClientProtocol):
    player: Player

    async def handle(self, ctx: Context):
        return await self.player.handle(ctx, STUDIO_21_URL)
