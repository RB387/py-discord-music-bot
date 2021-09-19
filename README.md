# Python Discord Music Bot
Easy to extend and support

## Supported commands
```
!play [url or name] - play song from any stream/video or youtube search
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

## TODO
* Write tests on bot business logic
* Add loop queue