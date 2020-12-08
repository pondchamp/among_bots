from typing import List

from clients import monitor, tts, keyboard
from clients.pcap import game_state
from controller import response
from data import enums, consts
from data.state import context


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
            elif mode is not None:
                flags = _get_response_flags()
                resp = response.generate_response(mode, game_state.get_map(), context.get_player_sus(), flags)
                if resp != '':
                    if not _in_game():
                        continue
                    tts.Speaker(resp)
                    keyboard.write_text(resp)
                    chat_turns = context.get_chat_turns()
                    print(f"Response #{chat_turns}: {resp}")
                    context.set_chat_turns(chat_turns + 1)


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
        else:
            if start_by.playerId == me.playerId:
                flags.append(enums.ResponseFlags.BODY_FOUND_ME)
            else:
                flags.append(enums.ResponseFlags.BODY_FOUND_OTHER)

    return flags
