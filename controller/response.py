from typing import List
import random
import re

from controller.substitutions import Substitutions
from data import enums, dialogs


def generate_response(mode: enums.KeyCommands, curr_map: enums.AUMap, players: List[str]) -> str:
    if mode == enums.KeyCommands.ATTACK:
        mode_arr = dialogs.attack
    elif mode == enums.KeyCommands.DEFENCE:
        mode_arr = dialogs.defense
    elif mode == enums.KeyCommands.PROBE:
        mode_arr = dialogs.probe
    elif mode == enums.KeyCommands.STATEMENT:
        mode_arr = dialogs.statement
    else:
        return ''

    i = random.randint(0, len(mode_arr) - 1)
    resp_sub = sub_placeholders(mode_arr[i], curr_map, players)
    return resp_sub


def sub_placeholders(resp: str, curr_map: enums.AUMap, players: List[str]) -> str:
    subs = Substitutions(players)
    for sub in subs.substitutions:
        res = subs.get(curr_map, sub)
        i = random.randint(0, len(res) - 1)
        resp = re.sub(fr"\[{sub}]", res[i], resp)
    return resp
