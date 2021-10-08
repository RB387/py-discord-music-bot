import logging
from dataclasses import dataclass
from typing import Dict

from lib.core.injector import ClientProtocol, FileConstructable


@dataclass
class Logger(FileConstructable):
    CONFIG_NAME = 'logger'

    log: logging.Logger = logging.root

    @classmethod
    def __from_config__(
        cls, config: Dict[str, Dict], **clients: Dict[str, ClientProtocol]
    ) -> ClientProtocol:
        kwargs = config.get(cls.CONFIG_NAME, {})
        logging.basicConfig(**kwargs)

        return cls()

    def info(self, msg, *args, **kwargs):
        return self.log.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self.log.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return self.log.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self.log.warning(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        return self.log.exception(msg, *args, **kwargs)
