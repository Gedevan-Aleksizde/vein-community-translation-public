import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict

__dp_work = Path(__file__).parent.parent
__settings = json.load(__dp_work.joinpath("settings.json").open("r", encoding="utf-8"))


@dataclass
class Settings:
    """Class for keeping track of an item in inventory."""
    version: str
    inputdir: Path
    __settings: Dict
    def __init__(self, settings):
        self.version = settings["version"]
        self.inputdir = Path(settings["inputdir"])
        self__settings = settings


settings = Settings(__settings)