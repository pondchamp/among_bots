from enum import Enum
from typing import Optional


class KeyCommand(Enum):
    HELP = 'f1'
    AUTO = 'f2'
    ATTACK = 'f3'
    DEFENCE = 'f4'
    PROBE = 'f5'
    STATEMENT = 'f6'
    REPEAT = 'f7'
    DEBUG = 'f8'
    EXIT = 'f12'
    KEY_CAP = '`'


def get_key_command(key: str) -> Optional[KeyCommand]:
    try:
        return KeyCommand(key)
    except ValueError:
        return None


class Substitution(Enum):
    PLAYER = 'p'
    PLAYER_NEAREST = 'pn'
    LOCATION = 'l'
    LOCATION_ME = 'lm'
    LOCATION_BODY = 'lb'
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


class ResponseFlags(Enum):
    PRIORITY = -1
    BODY_FOUND_ME = 0
    BODY_FOUND_OTHER = 1
    EMERGENCY_MEET_ME = 2
    EMERGENCY_MEET_OTHER = 3
    SELF_REPORT = 4
    SELF_IMPOSTOR = 5
    SELF_SABOTAGE = 6
    ACCUSED_VENT = 7
