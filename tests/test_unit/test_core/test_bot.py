import asyncio
from asyncio import Lock

import pytest

from lib.core import DiscordBot


@pytest.mark.asyncio
async def test_consume_tasks(bot: DiscordBot):
    tasks_done = 0

    lock = Lock()
    await lock.acquire()

    async def _task():
        nonlocal tasks_done, lock
        async with lock:
            tasks_done += 1

    await bot.__connect__()

    await bot.queue_task('test_queue', _task)
    assert bot.qsize('test_queue') == 1

    await bot.queue_task('test_queue', _task)
    assert bot.qsize('test_queue') == 2

    lock.release()
    await asyncio.sleep(0)

    assert bot.qsize('test_queue') == 0
    assert tasks_done == 2
    await asyncio.wait_for(bot.join_queue('test_queue'), timeout=0.1)
