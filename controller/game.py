import datetime
import random
import re
from typing import Optional

from clients import monitor, tts, keyboard
from controller import response, helpers
from controller.callbacks import Callbacks
from controller.response import get_strategy
from data import enums, consts, params
from state.context import context
from state.game import GameState


def start_game():
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to disable key capture.\n')
    print_commands()
    while True:
        key = keyboard.get_char()
        if key is not None:
            mode = handle_key(key)
            if mode == enums.KeyCommand.HELP:
                print_commands()
            elif mode == enums.KeyCommand.EXIT:
                break
            elif mode == enums.KeyCommand.DEBUG:
                _toggle_debug()
            elif mode == enums.KeyCommand.REPEAT:
                last_phrase = context.last_phrase
                if last_phrase is not None:
                    _output_phrase(last_phrase)
                else:
                    print('No chat history to repeat.')
            elif mode is not None:
                if not _wait_timer(consts.CHAT_THROTTLE_SECS):
                    continue
                debug = context.debug
                try:
                    me = game_state.me_colour if game_state.me is not None else helpers.get_me().name.lower()
                except IOError:
                    print('Cannot find player preferences file. Have you installed Among Us?')
                    me = None
                if not game_state.map:
                    if debug:
                        print('DEBUG: defaulting to Skeld')
                        game_state.map = enums.AUMap.SKELD
                    else:
                        print('Game state not loaded - wait for next discussion time or game round.')
                        continue
                if len(context.trust_map_score_get()) == 0:
                    if debug:
                        print('DEBUG: defaulting to all players')
                        players = params.player
                        context.trust_map_players_set(players)
                        context.trust_map_score_set(me, players[random.randint(0, len(players) - 1)], -0.5)
                        game_state.set_player_loc()
                    else:
                        print('Wait until discussion time before attempting to chat.')
                        continue
                if mode == enums.KeyCommand.AUTO:
                    mode = get_strategy(game_state)
                    if mode is None:
                        print("You can't speak if you're dead!")
                        continue
                resp = response.generate_response(mode, game_state.map, me, game_state.get_response_flags())
                if resp is not None:
                    _output_phrase(resp)
                else:
                    print("No responses currently available for this option.")


def handle_key(key: str) -> Optional[enums.KeyCommand]:
    mode = enums.get_key_command(key)
    if mode is None:
        return None

    if context.capture_keys or mode == enums.KeyCommand.KEY_CAP:
        keyboard.backspace()
        if mode == enums.KeyCommand.KEY_CAP:
            context.capture_keys = not context.capture_keys
            print("KEY CAPTURE", "ENABLED" if context.capture_keys else "DISABLED")
            if context.capture_keys:
                print_commands()
        else:
            return mode


def _output_phrase(resp: str):
    chat_turns = context.chat_turns
    print(f"Response #{chat_turns}: {resp}", end='\n\n')
    context.last_phrase = resp
    context.update_state(game_state, callbacks.root_dir)
    if not _in_game():
        return
    tts.Speaker(resp, emphasis=keyboard.caps_enabled(), use_gcp=context.use_gcp)
    keyboard.write_text(_strip(resp))


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE


def _wait_timer(wait_secs: int) -> bool:
    if context.debug:
        return True
    last_response = context.last_response
    wait_time = datetime.timedelta(seconds=wait_secs)
    new_last_response = datetime.datetime.now()
    if last_response is not None and last_response + wait_time > new_last_response:
        return False
    context.last_response = new_last_response
    return True


def _strip(text: str) -> str:
    return re.sub(r'[^a-z0-9]$', '', text)


def _toggle_debug():
    context.debug = not context.debug
    print(f'DEBUG MODE {"ENABLED" if context.debug else "DISABLED"}')


def print_commands():
    print("COMMANDS")
    for x in [x for x in enums.KeyCommand if x != enums.KeyCommand.KEY_CAP]:
        k = str.upper(x.value)
        v = str.title(x.name).replace('_', ' ')
        print(f'{k}\t:', v)
    print()


game_state: GameState = GameState()
callbacks = Callbacks(game_state)
game_state.cb = callbacks.cb
