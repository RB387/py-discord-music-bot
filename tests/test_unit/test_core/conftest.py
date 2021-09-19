from unittest.mock import MagicMock

import pytest

from lib.core import DiscordBot
from lib.core.injector import DependencyInjector


@pytest.fixture
def injector():
    inject_value = 1337
    config = {'common': {'value': inject_value}}

    return DependencyInjector(config)


@pytest.fixture
def bot():
    return DiscordBot(
        queues=[{'name': 'test_queue'}],
        logger=MagicMock(),
        command_prefix='-',
    )
