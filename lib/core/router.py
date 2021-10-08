from dataclasses import dataclass, field
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    List,
    Protocol,
    Type,
    TypeVar,
)


class HandlerProtocol(Protocol):
    handle: Callable[[Any], Awaitable[None]]


T = TypeVar('T')


@dataclass(frozen=True)
class _CommandRoute(Generic[T]):
    handler: Type[T]
    name: str


@dataclass(frozen=True)
class _EventRoute(Generic[T]):
    handler: Type[T]
    name: str


@dataclass(frozen=True)
class _Routes:
    events: Iterable[_EventRoute]
    commands: Iterable[_CommandRoute]


@dataclass
class Router:
    name: str = 'Common'
    _events: List[_EventRoute] = field(default_factory=list)
    _commands: List[_CommandRoute] = field(default_factory=list)

    def event(self, name: str) -> Callable[[Type[T]], Type[T]]:
        def _deco(cls: Type[T]) -> Type[T]:
            self._events.append(_EventRoute(cls, name))
            return cls

        return _deco

    def command(self, name: str) -> Callable[[Type[T]], Type[T]]:
        def _deco(cls: Type[T]) -> Type[T]:
            self._commands.append(_CommandRoute(cls, name))
            return cls

        return _deco

    def get_routes(self) -> _Routes:
        return _Routes(
            events=tuple(self._events),
            commands=tuple(self._commands),
        )


router = Router()
