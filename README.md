# Python Discord Music Bot
Easy to extend and support

![Bot play](https://raw.githubusercontent.com/RB387/py-discord-music-bot/master/.git_images/play.png)


## Supported commands
```
!play [url or name] - play song from any stream/video or youtube search
!loop - enable/disable queue loop
!queue - current bot song queue
!pause - pause current song
!resume - resume paused song
!skip - skip current song
!clear - clear bot queue
!message-clean - clear bot messages
!studio21 - play radio studio21
!21queue - show studio21 queue 
```

## Background queue tasks
Just add queue in config.toml
```python
bot: DiscordBot

async def task():
    print('done in background')
    
await bot.add_task('my_queue', task)
```

## Configuration
All bot configuration in config.toml  
The only exception is secrets. They must be set in environment or in file .env:
```
DISCORD_TOKEN -- bot token
```

## MacOS Installation
```
brew install ffmpeg
pip intall -r requirements.txt
```

## Run
### Docker
```
docker build -t discord-music-bot .
docker run discord-music-bot
```
### Local
```
python main.py
```

## Tests
```
pip install -r test-requirements.txt
pytest tests/
```

## How to add new command
Just create new class with `handle` method and add `router.command` decorator    

To register this command import it in `lib/commands/__init__.py`    

For auto help generation add `__doc__` for your new command

## Dependency Injection
You can create commands with dependencies  
 
All you need is just add them to class signature  
Injector will resolve and inject all classes with magic methods `__connect__`, `__disconnect__` from `ClientProtocol` interface

Also, you can initialize clients from config. Just add `__from_config__` method from `FileConstructable` interface

#### Example
```python
from dataclasses import dataclass
from lib.core.injector import ClientProtocol
from lib.core.router import router


class MyClient(ClientProtocol):
    def do(self):
        print('DID SOMETHING')


@router.command('command')
@dataclass
class MyCommand:
    client: MyClient  # will be auto injected

    async def handle(self, ctx):
        self.client.do()
```

## TODO
* Write tests on bot business logic