from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

from discord import Message as DiscordMessage
from discord.ext.commands import Context

from lib.core.bot import DiscordBot
from lib.core.injector import FileConstructable
from lib.core.response import Response
from lib.emoji import Emoji
from lib.templates import TemplateStorage

_DEFAULT = object()


@dataclass(frozen=True)
class Message:
    template_name: str
    args: Tuple[Any, ...] = ()


@dataclass
class Messenger(FileConstructable):
    response_kwargs: Dict[str, Any]
    messages_ttl: int
    templates: TemplateStorage
    bot: DiscordBot

    @classmethod
    def __from_config__(cls, config: Dict[str, Dict], **clients) -> 'Messenger':
        response_kwargs = config['response']
        messages_ttl = config['common']['messages_ttl']

        return cls(response_kwargs=response_kwargs, messages_ttl=messages_ttl, **clients)

    async def send(
        self,
        ctx: Context,
        title: str,
        msgs: List[Message],
        delete_after: Optional[int] = _DEFAULT,  # type: ignore
    ):
        if delete_after is _DEFAULT:
            delete_after = self.messages_ttl

        content = []
        for msg in msgs:
            template = self.templates.get(msg.template_name)
            content.append(template.format(*msg.args))

        response = Response(
            title=title,
            content=''.join(content),
            user=self.bot.user,
            **self.response_kwargs,
        )

        await ctx.send(embed=response.render(), delete_after=delete_after)

    @staticmethod
    async def react(ctx: Context, emoji: Emoji):
        message: DiscordMessage = ctx.message
        await message.add_reaction(emoji.value)
