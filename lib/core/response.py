from dataclasses import dataclass

import discord
from discord import User


@dataclass
class Response:
    title: str
    content: str
    user: User
    colour: int

    footer_img: str
    footer_text: str
    author_url: str

    def render(self) -> discord.Embed:
        embed = discord.Embed(colour=self.colour, title=self.title, description=self.content)

        embed.set_footer(text=self.footer_text, icon_url=self.footer_img)
        embed.set_author(
            name=self.user.name,
            url=self.author_url,
            icon_url=self.user.avatar.url,
        )

        return embed
