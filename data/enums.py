from enum import Enum
from typing import Optional


class KeyCommands(Enum):
    ATTACK = 'a'
    DEFENCE = 'd'
    PROBE = 'w'
    STATEMENT = 's'
    RESTART = 'r'
    REFRESH = 'x'
    KEY_CAP = '`'


def get_key_command(key: str) -> Optional[KeyCommands]:
    try:
        return KeyCommands(key[0])
    except ValueError:
        return None


class GameState(Enum):
    SETUP = 0
    PROGRESS = 1
    RESTART = 2


class AUMap(Enum):
    COMMON = -1
    SKELD = 0
    POLUS = 1
    MIRA = 2
