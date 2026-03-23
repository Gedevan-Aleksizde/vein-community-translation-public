import json
import re
from dataclasses import dataclass
from pathlib import Path
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

    def __repr__(self):
        return str({"version": self.version, "inputdir": self.inputdir})


PAT_EQ = re.compile("^(.+?)=(.+)$")


def parse_bat(fp: Path):
    raw = fp.read_text(encoding="utf-8")
    vars = [PAT_EQ.match(x[4:]).groups(0) for x in raw.split("\n") if x[:3] == "SET"]
    return dict(vars)


params_bat = parse_bat(Path(__file__).parent.parent.parent.joinpath("bin/settings.bat"))
__settings["version"] = params_bat["VER"]
settings = Settings(__settings)
