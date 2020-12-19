import os
from enum import Enum
from typing import Optional

from data.enums import PlayerColour


def get_me() -> PlayerColour:
    file_path = os.environ['USERPROFILE'] + r'\AppData\LocalLow\Innersloth\Among Us\playerPrefs'
    with open(file_path, 'r') as f:
        contents = f.read()
        me_colour = contents.split(',')[2]
        return PlayerColour.__call__(int(me_colour))


class NumKey(Enum):
    N10 = '0'
    N11 = '-'
    N12 = '+'
    N13 = '['
    N14 = ']'
    N15 = '\\'


def num_to_key(num: int) -> Optional[str]:
    if 1 <= num < 10:
        return str(num)
    elif num == 10:
        return str(NumKey.N10.value)
    elif num == 11:
        return str(NumKey.N11.value)
    elif num == 12:
        return str(NumKey.N12.value)
    elif num == 13:
        return str(NumKey.N13.value)
    elif num == 14:
        return str(NumKey.N14.value)
    elif num == 15:
        return str(NumKey.N15.value)
    else:
        return None


def key_to_num(key: str) -> Optional[int]:
    if '1' <= key <= '9':
        return int(key)
    elif key == str(NumKey.N10.value):
        return 10
    elif key == str(NumKey.N11.value):
        return 11
    elif key == str(NumKey.N12.value):
        return 12
    elif key == str(NumKey.N13.value):
        return 13
    elif key == str(NumKey.N14.value):
        return 14
    elif key == str(NumKey.N15.value):
        return 15
    else:
        return None
