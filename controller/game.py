import datetime
import re
from typing import List

from clients import monitor, tts, keyboard
from clients.pcap import game_state
from controller import response
from data import enums, consts, params
from data.state import context
from data.sus_score import SusScore


def start_game():
    print('\nGAME STARTED!')
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to enable bot commands.\n')
    while True:
        key = keyboard.get_char()
        if key is not None:
            mode = keyboard.handle_key(key)
            if mode == enums.KeyCommand.HELP:
                keyboard.print_commands()
                print()
            elif mode == enums.KeyCommand.DEBUG:
                debug = context.get_debug()
                debug = not debug
                context.set_debug(debug)
                print(f'DEBUG MODE {"ENABLED" if debug else "DISABLED"}')
            elif mode == enums.KeyCommand.REPEAT:
                last_phrase = context.get_last_phrase()
                if last_phrase is not None:
                    _output_phrase(last_phrase)
                else:
                    print('No chat history to repeat.')
            elif mode is not None:
                if not wait_timer(consts.CHAT_THROTTLE_SECS):
                    continue
                debug = context.get_debug()
                if not game_state.get_map():
                    if debug:
                        print('DEBUG: defaulting to Skeld')
                        game_state.set_map(enums.AUMap.SKELD)
                        curr_map = enums.AUMap.SKELD
                    else:
                        print('Game state not loaded - rejoin the lobby to sync game settings.')
                        return ''
                if not context.get_player_sus():
                    if debug:
                        print('DEBUG: defaulting to all players')
                        game_state.set_player_sus(params.player)
                        game_state.set_player_loc()
                    else:
                        print('Wait until discussion time before attempting to chat.')
                        return ''
                flags = _get_response_flags()
                resp = response.generate_response(mode, game_state.get_map(), context.get_player_sus(), flags)
                if resp != '':
                    _output_phrase(resp)
                else:
                    print(f"No responses currently available for this option.")


def _output_phrase(resp: str):
    chat_turns = context.get_chat_turns()
    print(f"Response #{chat_turns}: {resp}")
    context.set_last_phrase(resp)
    if not _in_game():
        return
    tts.Speaker(resp, emphasis=keyboard.caps_enabled())
    keyboard.write_text(_strip(resp))


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE


def _get_response_flags() -> List[enums.ResponseFlags]:
    flags = []
    me = game_state.get_me()
    reason = game_state.get_meeting_reason()
    start_by = game_state.get_meeting_started_by()
    if reason and start_by:
        if reason == 'Button':
            if start_by.playerId == me.playerId:
                flags.append(enums.ResponseFlags.EMERGENCY_MEET_ME)
            else:
                flags.append(enums.ResponseFlags.EMERGENCY_MEET_OTHER)
        else:  # Body found
            if start_by.playerId == me.playerId:
                flags.append(enums.ResponseFlags.BODY_FOUND_ME)
            else:
                flags.append(enums.ResponseFlags.BODY_FOUND_OTHER)
                player_colour = game_state.get_player_from_id(start_by.playerId)
                if player_colour in [p.player for p in context.get_player_sus() if p.get_sus() == SusScore.SUS]:
                    flags.append(enums.ResponseFlags.SELF_REPORT)

    return flags


def wait_timer(wait_secs: int) -> bool:
    if context.get_debug():
        return True
    last_response = context.get_last_response()
    wait_time = datetime.timedelta(seconds=wait_secs)
    new_last_response = datetime.datetime.now()
    if last_response is not None and last_response + wait_time > new_last_response:
        return False
    context.set_last_response(new_last_response)
    return True


def _strip(text: str) -> str:
    return re.sub(r'[^a-z0-9]$', '', text)
