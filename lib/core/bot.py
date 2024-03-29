import asyncio
import os
from asyncio import Queue as BaseQueue
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
)

from discord import Client, Intents
from discord.ext.commands import Bot as BaseBot

from lib.core.injector import ClientProtocol, FileConstructable
from lib.core.logger import Logger

INTENTS = {
    "all": Intents.all(),
    "default": Intents.default(),
    "none": Intents.none(),
}


class Queue(BaseQueue):
    def clear_queue(self):
        while not self.empty():
            self.get_nowait()
            self.task_done()


class DiscordBot(BaseBot, FileConstructable):
    CONFIG_NAME = 'bot'

    def __init__(self, *args, logger: Logger, disconnect_timeout: float = 5.0, intents: Intents, **kwargs):
        Client.__init__(self, **kwargs, intents=intents)
        super().__init__(*args, **kwargs, intents=intents)

        self._queues: Dict[str, Queue] = {}
        self._logger = logger

        self._disconnect_timeout = disconnect_timeout
        self._consumers: List[asyncio.Task] = []

        self.on_startup: List[Callable] = []
        self.on_shutdown: List[Callable] = []

    @classmethod
    def __from_config__(cls, config: Dict[str, Dict], **clients) -> ClientProtocol:
        kwargs: Dict[str, Any] = config.get(cls.CONFIG_NAME, {})
        intents = kwargs.pop("intents", None) or "default"
        return cls(**kwargs, intents=INTENTS[intents], **clients)

    async def __disconnect__(self):
        for consumer in self._consumers:
            consumer.cancel()

        if self._consumers:
            await asyncio.wait(self._consumers, timeout=self._disconnect_timeout)

    def run(self, token: Optional[str] = None, **kwargs):
        if not token:
            token = os.environ['DISCORD_TOKEN']

        super().run(token, **kwargs)

    async def start(self, *args, **kwargs):
        await self._do_startup()

        try:
            await super().start(*args, **kwargs)
        finally:
            await self._do_shutdown()

    async def queue_task(self, queue_name: str, task: Callable[[], Awaitable]) -> int:
        if queue_name not in self._queues:
            queue = Queue()
            self._queues[queue_name] = queue
            await self._consume_queue(queue)
        else:
            queue = self._queues[queue_name]

        await queue.put(task)
        return self.qsize(queue_name)

    def qsize(self, queue_name: str) -> int:
        return self._queues[queue_name].qsize()

    async def join_queue(self, queue_name: str):
        await self._queues[queue_name].join()

    def clear_queue(self, queue_name: str):
        q = self._queues.get(queue_name)
        if q:
            q.clear_queue()

    async def _do_startup(self):
        for handler in self.on_startup:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def _do_shutdown(self):
        for handler in self.on_shutdown:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception:
                self._logger.exception('Failed to execute on shutdown handler')

    async def _consume_queue(self, q: Queue):
        async def _consume():
            while self.loop.is_running():
                task = await q.get()

                try:
                    await task()
                except Exception:
                    self._logger.exception('Failed to execute task')

                q.task_done()

            self._logger.info('Finished consuming')

        consumer = asyncio.create_task(_consume())
        self._consumers.append(consumer)
