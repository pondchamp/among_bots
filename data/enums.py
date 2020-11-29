from enum import Enum
from typing import Optional


class KeyCommand(Enum):
    REFRESH = '1'
    ATTACK = '2'
    DEFENCE = '3'
    PROBE = '4'
    STATEMENT = '5'
    CHANGE_PLAYER = '6'
    CHANGE_IMPOSTOR_COUNT = '7'
    CHANGE_MAP = '8'
    HELP = '0'
    KEY_CAP = '`'


def get_key_command(key: str) -> Optional[KeyCommand]:
    try:
        return KeyCommand(key[0])
    except ValueError:
        return None


class Substitution(Enum):
    PLAYER = 'p'
    LOCATION = 'l'
    TASK = 't'


class AUMap(Enum):
    COMMON = -1
    SKELD = 0
    POLUS = 1
    MIRA = 2
