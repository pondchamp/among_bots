from typing import List
import random
import re

from controller.substitute import SubstituteHelper
from data import enums, dialogs
from data.state import context
from data.sus_score import PlayerSus, SusScore


def generate_response(mode: enums.KeyCommand, curr_map: enums.AUMap, players: List[PlayerSus],
                      flags: List[enums.ResponseFlags]) -> str:
    if not curr_map:
        print('Game state not loaded - rejoin the lobby to sync game settings.')
        return ''
    if not players:
        print('Wait until discussion time before attempting to chat.')
        return ''

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

    chat_turns = context.get_chat_log()
    curr_turns = context.get_chat_turns()
    pri_arr = [[x.text for x in mode_arr
                if x.max_turns is not None and x.max_turns >= curr_turns
                and x.flags is not None and len(set(flags) & set(x.flags)) > 0],
               [x.text for x in mode_arr
                if x.max_turns is not None and x.max_turns >= curr_turns],
               [x.text for x in mode_arr if x.max_turns is None]]
    for arr in pri_arr:
        if len(arr) > 0:
            mode_arr = arr
            break

    resp_sub = ''
    m = mode_arr.copy()
    while resp_sub == '':
        if len(m) == 0:
            chat_turns = []
            context.chat_log_clear()
            m = mode_arr.copy()
            continue
        r = m[random.randint(0, len(m) - 1)]
        if r not in chat_turns:
            context.chat_log_append(r)
            resp_sub = sub_placeholders(r, curr_map, player_select)
        m.remove(r)
    return resp_sub


def sub_placeholders(resp: str, curr_map: enums.AUMap, players: List[str]) -> str:
    subs = SubstituteHelper(players)
    for sub in subs.substitutions:
        res = subs.get(curr_map, sub)
        i = random.randint(0, len(res) - 1)
        resp = re.sub(fr"\[{sub.value}]", res[i], resp)
    return resp
