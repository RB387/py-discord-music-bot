import logging
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    Protocol,
    Type,
    TypeVar,
    get_type_hints,
    runtime_checkable,
)


@runtime_checkable
class ClientProtocol(Protocol):
    async def __connect__(self):
        ...

    async def __disconnect__(self):
        ...


@runtime_checkable
class FileConstructable(ClientProtocol, Protocol):
    @classmethod
    def __from_config__(
        cls, config: Dict[str, Dict], **clients: Dict[str, 'ClientProtocol']
    ) -> 'ClientProtocol':
        ...


def is_client(cls: Type[ClientProtocol]) -> bool:
    try:
        return issubclass(cls, ClientProtocol)
    except TypeError:
        return False


T = TypeVar('T')


def _is_class(obj: Any) -> bool:
    return isinstance(obj, type)


@dataclass
class DependencyInjector:
    config: Dict[str, Dict]
    _deps: Dict[Type[T], T] = field(init=False, default_factory=dict)  # type: ignore

    def inject(self, cls: Type[T]) -> T:
        if instance := self._deps.get(cls):
            return instance  # type: ignore

        hints = get_type_hints(cls.__init__)

        clients = {}

        for name, hint in hints.items():
            if not is_client(hint):
                continue

            instance = self.inject(hint)
            clients[name] = instance

        if issubclass(cls, FileConstructable):
            self._deps[cls] = cls.__from_config__(self.config, **clients)
        else:
            self._deps[cls] = cls(**clients)  # type: ignore

        return self._deps[cls]

    async def connect(self):
        for cls, instance in self._deps.items():
            if is_client(cls):
                logging.debug(f'Connecting {cls}...')
                await instance.__connect__()

    async def disconnect(self):
        for cls, instance in reversed(list(self._deps.items())):
            if is_client(cls):
                try:
                    await instance.__disconnect__()
                except Exception:
                    logging.exception('Failed to disconnect')
