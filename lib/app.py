from asyncio import Lock
from typing import Type

from lib.core.bot import DiscordBot
from lib.core.injector import DependencyInjector
from lib.core.logger import Logger
from lib.core.router import Router, router as default_router


async def _wait_forever():
    """ just wait forever until loop is not closed """
    lock = Lock()
    await lock.acquire()
    await lock.acquire()
    print('out')


class App:
    def __init__(
        self,
        injector: DependencyInjector,
        bot_cls: Type[DiscordBot] = DiscordBot,
    ):

        self._injector = injector
        self._bot = injector.inject(bot_cls)
        self._logger = injector.inject(Logger)
        self._routers = [default_router]

    def run(self):
        self._setup_routes()

        self._bot.listen('on_connect')(self._injector.connect)
        self._bot.listen('on_disconnect')(self._injector.disconnect)

        self._logger.info('Running bot...')
        self._bot.run()

    def add_router(self, router: Router):
        self._routers.append(router)

    def _setup_routes(self):
        for router in self._routers:
            routes = router.get_routes()

            for event in routes.events:
                handler = self._injector.inject(event.handler)
                self._bot.listen(event.name)(handler.handle)

            for command in routes.commands:
                handler = self._injector.inject(command.handler)
                self._bot.command(name=command.name)(handler.handle)
