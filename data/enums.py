from enum import Enum
from typing import Optional


class KeyCommand(Enum):
    ATTACK = 'f1'
    DEFENCE = 'f2'
    PROBE = 'f3'
    STATEMENT = 'f4'
    HELP = 'esc'
    KEY_CAP = '`'


def get_key_command(key: str) -> Optional[KeyCommand]:
    try:
        return KeyCommand(key)
    except ValueError:
        return None


class Substitution(Enum):
    PLAYER = 'p'
    LOCATION = 'l'
    TASK = 't'


class AUMap(Enum):
    COMMON = -1
    SKELD = 0
    MIRA = 1
    POLUS = 2


# https://wiki.weewoo.net/wiki/Enums
class PlayerColour(Enum):
    Red = 0
    Blue = 1
    Green = 2
    Pink = 3
    Orange = 4
    Yellow = 5
    Black = 6
    White = 7
    Purple = 8
    Brown = 9
    Cyan = 10
    Lime = 11
