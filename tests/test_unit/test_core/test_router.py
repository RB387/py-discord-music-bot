from lib.core.router import (
    Router,
    _CommandRoute,
    _EventRoute,
    _Routes,
)


async def event_one():
    ...


async def event_two():
    ...


async def command_one():
    ...


async def command_two():
    ...


def test_router():
    router = Router()

    router.event('one')(event_one)
    router.event('two')(event_two)
    router.command('one')(command_one)
    router.command('two')(command_two)

    assert router.get_routes() == _Routes(
        events=(
            _EventRoute(handler=event_one, name='one'),
            _EventRoute(handler=event_two, name='two'),
        ),
        commands=(
            _CommandRoute(handler=command_one, name='one'),
            _CommandRoute(handler=command_two, name='two'),
        ),
    )
