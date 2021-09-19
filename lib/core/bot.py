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

from discord.ext.commands import Bot as BaseBot

from lib.core.injector import ClientProtocol, FileConstructable
from lib.core.logger import Logger


class Queue(BaseQueue):
    async def clear_queue(self):
        while not self.empty():
            self.get_nowait()
            self.task_done()


class DiscordBot(BaseBot, FileConstructable):
    CONFIG_NAME = 'bot'

    def __init__(self, *args, queues: List, logger: Logger, **kwargs):
        super().__init__(*args, **kwargs)

        self._queues: Dict[str, Queue] = {}
        self._logger = logger

        for q_config in queues:
            name = q_config['name']
            self._queues[name] = Queue()

        self._running = False
        self._consumers: List[asyncio.Task] = []

    @classmethod
    def from_config(cls, config: Dict[str, Dict], **clients) -> ClientProtocol:
        kwargs: Dict[str, Any] = config.get(cls.CONFIG_NAME, {})
        return cls(**kwargs, **clients)

    def run(self, token: Optional[str] = None, **kwargs):
        if not token:
            token = os.environ['DISCORD_TOKEN']

        super().run(token, **kwargs)

    async def __connect__(self):
        await self._consume_tasks()

    async def add_task(self, queue_name: str, task: Callable[[], Awaitable]) -> int:
        queue = self._queues[queue_name]
        await queue.put(task)

        return self.qsize(queue_name)

    def qsize(self, queue_name: str) -> int:
        return self._queues[queue_name].qsize()

    async def join_queue(self, queue_name: str):
        await self._queues[queue_name].join()

    async def clear_queue(self, queue_name: str):
        q = self._queues[queue_name]
        await q.clear_queue()

    async def _consume_tasks(self):
        async def _consume_queue(q: Queue):
            while self.loop.is_running():
                task = await q.get()

                try:
                    await task()
                except Exception:
                    self._logger.exception('Failed to execute task')

                q.task_done()

        for q in self._queues.values():
            consumer = asyncio.create_task(_consume_queue(q))
            self._consumers.append(consumer)
