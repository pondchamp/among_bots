import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener

from controller import response
from data import enums
from data.state import context

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener(on_release=on_release)


def handle_key(key: str):
    game_state = context.get_state_game()
    state_map = context.get_state_map()
    state_players = context.get_state_players()

    if game_state == enums.GameState.PROGRESS:
        mode = enums.get_key_command(key)
        if mode is None:
            return
        capture_keys = context.get_capture_keys()
        if capture_keys or mode == enums.KeyCommands.KEY_CAP:
            keyboard_controller.press(Key.backspace)
            if mode == enums.KeyCommands.KEY_CAP:
                context.set_capture_keys(not capture_keys)
                print(f'KEY CAPTURE {"NOT " if capture_keys else ""}ENABLED')
            elif mode == enums.KeyCommands.RESTART:
                context.set_state_game(enums.GameState.RESTART)
            elif mode == enums.KeyCommands.KILL:
                print(f'Remaining players:')
                for i in range(len(state_players)):
                    print(f'{i}: {state_players[i]}')
                print(f"Who died? ")
                context.set_state_game(enums.GameState.KILL_SELECT)
            else:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    for key in resp:
                        time.sleep(0.01)
                        keyboard_controller.press(key)
                    time.sleep(0.1)
                    keyboard_controller.press(Key.enter)
    elif game_state == enums.GameState.KILL_SELECT:
        keyboard_controller.press(Key.backspace)
        print()
        key_int = -1
        try:
            key_int = int(key)
        except ValueError:
            pass
        if 0 <= key_int < len(state_players):
            d_index = state_players[key_int]
            state_players.remove(d_index)
            context.set_state_players(state_players)
            print(f'Killed {d_index}.')
            if len(state_players) == 0:
                print('No more players remain.')
                context.set_state_game(enums.GameState.RESTART)
            else:
                context.set_state_game(enums.GameState.PROGRESS)
            return
        print('Invalid input.')
        context.set_state_game(enums.GameState.PROGRESS)


def get_char() -> Optional[str]:
    with Events() as events:
        event = events.get()
    if type(event) != Events.Press:
        return None
    return key_to_char(event.key)


def pop_char() -> Optional[str]:
    char = get_char()
    keyboard_controller.press(Key.backspace)
    return char


def key_to_char(key: Key) -> Optional[str]:
    if not hasattr(key, 'char'):
        return None
    return key.char


def on_release(key: Key):
    if context.get_state_game() == enums.GameState.RESTART and hasattr(key, 'char') and key.char == 'r':
        keyboard_controller.press(Key.backspace)
        return False
    return True
