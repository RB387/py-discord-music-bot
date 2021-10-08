from dataclasses import dataclass
from typing import Dict

import pytest

from lib.core import ClientProtocol, FileConstructable
from lib.core.injector import DependencyInjector


@dataclass
class ClientFromFile(FileConstructable):
    value: int

    @classmethod
    def __from_config__(cls, config: Dict[str, Dict], **clients):
        return cls(value=config['common']['value'])


@dataclass
class ClientConnectable(ClientProtocol):
    file_client: ClientFromFile
    connected: bool = False

    async def __connect__(self):
        self.connected = True

    async def __disconnect__(self):
        self.connected = False


def test_inject(injector: DependencyInjector):
    client = injector.inject(ClientConnectable)
    assert isinstance(client.file_client, ClientFromFile)

    assert client.file_client.value == 1337

    another_file_client = injector.inject(ClientFromFile)
    assert another_file_client is client.file_client


@pytest.mark.asyncio
async def test_injector_connect(injector: DependencyInjector):
    client = injector.inject(ClientConnectable)
    assert not client.connected

    await injector.connect()
    assert client.connected

    await injector.disconnect()
    assert not client.connected
