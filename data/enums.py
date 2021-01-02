from enum import Enum
from typing import Optional, List
from data import consts


# Underscore suffix for debug-only enum options
class KeyCommand(Enum):
    HELP = 'f1'
    TALK = 'f2'  # Auto-pick strategy
    ATTACK_ = 'f3'
    DEFENCE_ = 'f4'
    PROBE_ = 'f5'
    STATEMENT_ = 'f6'
    REPEAT = 'f7'
    DEBUG_ = 'f8'
    EXIT = 'f12'
    KEY_CAP = '`'


def get_key_commands() -> List[KeyCommand]:
    return [k for k in KeyCommand if _debug_only(k)]


def get_key_command(key: str) -> Optional[KeyCommand]:
    try:
        return KeyCommand(key) if _debug_only(key) else None
    except ValueError:
        return None


def _debug_only(key: str):
    return consts.debug_talk or not str(KeyCommand(key).name).endswith('_')


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
    BODY_NOT_LOCATED = 8
