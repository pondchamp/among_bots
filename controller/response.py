from typing import List, Optional, Dict
import random
import re

from controller.substitute import SubstituteHelper
from data import dialogs, consts, enums
from data.enums import KeyCommand, AUMap, ResponseFlags, Substitution
from data.state import context, get_response_flags
from data.trust import SusScore


def generate_response(mode: KeyCommand, curr_map: AUMap, me: str,
                      flags: List[ResponseFlags]) -> str:
    if mode == KeyCommand.ATTACK:
        mode_arr, score_target = dialogs.attack, SusScore.SUS
    elif mode == KeyCommand.DEFENCE:
        mode_arr, score_target = dialogs.defense, None
    elif mode == KeyCommand.PROBE:
        mode_arr, score_target = dialogs.probe, None
    elif mode == KeyCommand.STATEMENT:
        mode_arr, score_target = dialogs.statement, SusScore.SAFE
    else:
        return ''

    players = context.trust_map_score_get(me)
    player_select = [p for p in players]
    if score_target is not None:
        filtered = list(filter(lambda p: players[p] == score_target.value, player_select))
        player_select = filtered if len(filtered) > 0 else player_select

    chat_log = context.get_chat_log()
    chat_turns = context.get_chat_turns()
    pri_arr = [[x.text for x in mode_arr if _dialog_flags_match(x, flags) and _dialog_turns_valid(x, chat_turns)],
               [x.text for x in mode_arr if _dialog_flags_match(x, flags)
                and x.min_turns is None and x.max_turns is None],
               [x.text for x in mode_arr if x.flags is None and x.min_turns is None and x.max_turns is None]]
    pri_arr_filtered = [[x for x in pri_arr[i] if x not in chat_log] for i in range(len(pri_arr))]
    if consts.debug_chat:
        print("Scores:", players)
        print("Past messages:", chat_log)
        print("Flags:", [x.name for x in flags])
        print("Dialogs:", pri_arr)
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
    resp_sub, sub_dict = _sub_placeholders(r, curr_map, player_select)
    if mode == KeyCommand.ATTACK:
        p = None
        if Substitution.PLAYER in sub_dict:
            p = sub_dict[Substitution.PLAYER]
        elif Substitution.PLAYER_NEAREST in sub_dict:
            p = sub_dict[Substitution.PLAYER_NEAREST]
        if p is not None:
            context.trust_map_score_offset(me, p, -1.0)
    return resp_sub


def get_strategy(game_state) -> Optional[enums.KeyCommand]:
    valid = [enums.KeyCommand.PROBE, enums.KeyCommand.STATEMENT, enums.KeyCommand.ATTACK, enums.KeyCommand.DEFENCE]
    me = game_state.get_me()
    if me is not None and not me.alive:
        return None
    trust_scores = context.trust_map_score_get()
    me_score = trust_scores[game_state.get_me_colour()] \
        if len(trust_scores) > 0 and game_state.get_me_colour() else None
    score_sum = None
    trust_map = context.get_trust_map()
    if trust_map is not None:
        score_sum = 0.0
        for p in trust_map:
            score_sum += sum([abs(x) for x in trust_map[p].values()])
    players = game_state.get_players()
    flags = get_response_flags(game_state)
    chat_turns = context.get_chat_turns()
    if players is not None and len(players) == 2:  # three players left
        return enums.KeyCommand.ATTACK
    elif me_score is not None and me_score == SusScore.SUS:  # counter sus
        return enums.KeyCommand.DEFENCE
    elif score_sum is not None and score_sum < consts.PROBE_SCORE_THRESH:  # not enough info
        if chat_turns == 0:  # opener
            if _flags_match(flags, [ResponseFlags.EMERGENCY_MEET_ME, ResponseFlags.BODY_FOUND_ME]):
                return enums.KeyCommand.STATEMENT
            elif _flags_match(flags, [ResponseFlags.EMERGENCY_MEET_OTHER, ResponseFlags.BODY_FOUND_OTHER]):
                return enums.KeyCommand.PROBE
        return enums.KeyCommand.PROBE if random.randint(0, 1) == 0 else enums.KeyCommand.STATEMENT  # 50-50
    # enough info at this point
    elif len([p for p in trust_scores if trust_scores[p] == SusScore.SUS]) > 0:
        return enums.KeyCommand.ATTACK
    else:
        print('Unable to determine a strategy - picking at random.')
        return valid[random.randint(0, len(valid) - 1)]


def _sub_placeholders(resp: str, curr_map: AUMap, players: List[str]) -> (str, Dict):
    sub_dict = {}
    subs = SubstituteHelper(players)
    for sub in subs.substitutions:
        res = subs.get(curr_map, sub)
        i = random.randint(0, len(res) - 1)
        new_resp = re.sub(fr"\[{sub.value}]", res[i], resp)
        if new_resp != resp:
            sub_dict[sub] = res[i]
        resp = new_resp    return resp, sub_dict


def _dialog_turns_valid(dialog: dialogs.Dialog, chat_turns: int) -> bool:
    return (dialog.max_turns is None or dialog.max_turns >= chat_turns) \
       and (dialog.min_turns is None or dialog.min_turns <= chat_turns)


def _dialog_flags_match(dialog: dialogs.Dialog, flags: List[ResponseFlags]) -> bool:
    return dialog.flags is not None and _flags_match(dialog.flags, flags)


def _flags_match(a: List[ResponseFlags], b: List[ResponseFlags]) -> bool:
    return len(set(a) & set(b)) > 0
