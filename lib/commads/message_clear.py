from dataclasses import dataclass

from discord import Message
from discord.ext.commands import Context

from lib.core import (
    ClientProtocol,
    DiscordBot,
    router,
)


@router.command('message-clean')
@dataclass
class MessageCleaner(ClientProtocol):
    bot: DiscordBot

    async def handle(self, ctx: Context, *args):
        """ Clear all bot messages """

        def check(message: Message):
            return message.author == self.bot.user

        await ctx.channel.purge(check=check)
