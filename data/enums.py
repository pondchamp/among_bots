from enum import Enum
from typing import Optional


class KeyCommand(Enum):
    ATTACK = '1'
    DEFENCE = '2'
    PROBE = '3'
    STATEMENT = '4'
    RESTART = '5'
    REFRESH = '6'
    KEY_CAP = '`'


def get_key_command(key: str) -> Optional[KeyCommand]:
    try:
        return KeyCommand(key[0])
    except ValueError:
        return None


class GameState(Enum):
    SETUP = 0
    PROGRESS = 1
    RESTART = 2


class Substitution(Enum):
    PLAYER = 'p'
    LOCATION = 'l'
    TASK = 't'


class AUMap(Enum):
    COMMON = -1
    SKELD = 0
    POLUS = 1
    MIRA = 2
