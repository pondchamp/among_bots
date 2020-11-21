import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener

from clients import monitor
from controller import response
from data import enums, consts
from data.state import context

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener(on_release=on_release)


def handle_key(key: str):
    window_name = monitor.get_foreground_window()
    if window_name != consts.GAME_TITLE:
        return None

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
                capture_keys = not capture_keys
                context.set_capture_keys(capture_keys)
                print(f'{"DISCUSSION" if capture_keys else "GAME"} MODE')
                if capture_keys:
                    for k, v in [(x.value, str.lower(x.name)) for x in enums.KeyCommands if
                                 x != enums.KeyCommands.KEY_CAP]:
                        print(f'{k}: {v}')
                print()
            elif mode == enums.KeyCommands.RESTART:
                context.set_state_game(enums.GameState.RESTART)
            elif mode == enums.KeyCommands.REFRESH:
                players = monitor.get_players()
                me = context.get_state_me()
                if me in players:
                    players.remove(me)
                if players is not None and len(players) > 0:
                    context.set_state_players(players)
                    print(f'Set new player list: {players}')
                else:
                    print("Player list could not be obtained - " +
                          "make sure you're running this command in the voting panel with chat hidden.")
            else:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    for key in resp:
                        time.sleep(0.01)
                        keyboard_controller.press(key)
                    time.sleep(0.1)
                    keyboard_controller.press(Key.enter)


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
    if context.get_state_game() == enums.GameState.RESTART and key_to_char(key) == enums.KeyCommands.RESTART:
        keyboard_controller.press(Key.backspace)
        return False
    return True
