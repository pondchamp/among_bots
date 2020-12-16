from typing import List
import random
import re

from controller.substitute import SubstituteHelper
from data import enums, dialogs
from data.state import context
from data.sus_score import PlayerSus, SusScore


def generate_response(mode: enums.KeyCommand, curr_map: enums.AUMap, players: List[PlayerSus],
                      flags: List[enums.ResponseFlags]) -> str:
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

    chat_log = context.get_chat_log()
    chat_turns = context.get_chat_turns()
    pri_arr = [[x.text for x in mode_arr if _dialog_turns_valid(x, chat_turns) and _dialog_flags_match(x, flags)],
               [x.text for x in mode_arr if _dialog_flags_match(x, flags)],
               [x.text for x in mode_arr if x.flags is None and x.min_turns is None and x.max_turns is None]]
    pri_arr_filtered = [[x for x in pri_arr[i] if x not in chat_log] for i in range(len(pri_arr))]
    select_arr = -1
    for i in range(len(pri_arr)):
        if len(pri_arr_filtered[i]) > 0:
            select_arr = i
            break
    if select_arr == -1:
        context.chat_log_clear()
        pri_arr_filtered = pri_arr
    m = pri_arr_filtered[select_arr]
    r = m[random.randint(0, len(m) - 1)]
    context.chat_log_append(r)
    resp_sub = sub_placeholders(r, curr_map, player_select)
    return resp_sub


def sub_placeholders(resp: str, curr_map: enums.AUMap, players: List[str]) -> str:
    subs = SubstituteHelper(players)
    for sub in subs.substitutions:
        res = subs.get(curr_map, sub)
        i = random.randint(0, len(res) - 1)
        resp = re.sub(fr"\[{sub.value}]", res[i], resp)
    return resp


def _dialog_turns_valid(dialog: dialogs.Dialog, chat_turns: int) -> bool:
    return (dialog.max_turns is None or dialog.max_turns >= chat_turns) \
       and (dialog.min_turns is None or dialog.min_turns <= chat_turns)


def _dialog_flags_match(dialog: dialogs.Dialog, flags: List[enums.ResponseFlags]) -> bool:
    return dialog.flags is not None and len(set(flags) & set(dialog.flags)) > 0
