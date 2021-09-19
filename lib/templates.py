import json
from dataclasses import dataclass
from typing import Dict

from constants import TEMPLATES_PATH

from lib.core.injector import ClientProtocol, FileConstructable


@dataclass
class TemplateStorage(FileConstructable):
    templates: Dict[str, str]

    @classmethod
    def from_config(
        cls, config: Dict[str, Dict], **clients: Dict[str, ClientProtocol]
    ) -> ClientProtocol:
        language = config['language']
        templates_path = TEMPLATES_PATH / f'{language}.json'

        with open(templates_path, 'r') as f:
            return cls(templates=json.load(f))

    def get(self, name: str) -> str:
        return self.templates[name]
