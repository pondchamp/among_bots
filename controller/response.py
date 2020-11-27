from typing import List
import random
import re
import datetime

from controller.substitute import SubstituteHelper
from data import enums, dialogs, consts
from data.state import context
from data.sus_score import PlayerSus, SusScore


def generate_response(mode: enums.KeyCommand, curr_map: enums.AUMap, players: List[PlayerSus]) -> str:
    if not wait_timer(consts.CHAT_THROTTLE_SECS):
        return ''

    players = players if players is not None else []
    player_select: List[str] = [p.player for p in players]
    if mode == enums.KeyCommand.ATTACK:
        mode_arr = dialogs.attack
        player_select = [p.player for p in players if p.get_sus() == SusScore.SUS]
    elif mode == enums.KeyCommand.DEFENCE:
        mode_arr = dialogs.defense
    elif mode == enums.KeyCommand.PROBE:
        mode_arr = dialogs.probe
    elif mode == enums.KeyCommand.STATEMENT:
        mode_arr = dialogs.statement
        player_select = [p.player for p in players if p.get_sus() == SusScore.SAFE]
    else:
        return ''

    i = random.randint(0, len(mode_arr) - 1)
    resp_sub = sub_placeholders(mode_arr[i], curr_map, player_select)
    return resp_sub


def sub_placeholders(resp: str, curr_map: enums.AUMap, players: List[str]) -> str:
    subs = SubstituteHelper(players)
    for sub in subs.substitutions:
        res = subs.get(curr_map, sub)
        i = random.randint(0, len(res) - 1)
        resp = re.sub(fr"\[{sub.value}]", res[i], resp)
    return resp


def wait_timer(wait_secs: int) -> bool:
    last_response = context.get_last_response()
    wait_time = datetime.timedelta(seconds=wait_secs)
    new_last_response = datetime.datetime.now()
    if last_response is not None and last_response + wait_time > new_last_response:
        return False
    context.set_last_response(new_last_response)
    return True
