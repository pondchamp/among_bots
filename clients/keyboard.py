import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener

from data import enums
from data.state import context

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener(on_release=on_release)


def handle_key(key: str) -> Optional[enums.KeyCommand]:
    game_state = context.get_game()
    capture_keys = context.get_capture_keys()

    if game_state != enums.GameState.PROGRESS:
        return None

    mode = enums.get_key_command(key)
    if mode is None:
        return None

    if capture_keys or mode == enums.KeyCommand.KEY_CAP:
        backspace()
        if mode == enums.KeyCommand.KEY_CAP:
            capture_keys = not capture_keys
            context.set_capture_keys(capture_keys)
            print(f'KEY CAPTURE {"ENABLED" if capture_keys else "DISABLED"}')
            if capture_keys:
                for k, v in [(x.value, str.lower(x.name)) for x in enums.KeyCommand if
                             x != enums.KeyCommand.KEY_CAP]:
                    print(f'{k}: {v}')
            print()
        else:
            return mode


def write_text(text: str):
    for key in text:
        time.sleep(0.01)
        keyboard_controller.press(key)
    time.sleep(0.1)
    keyboard_controller.press(Key.enter)


def backspace():
    keyboard_controller.press(Key.backspace)


def get_char() -> Optional[str]:
    with Events() as events:
        event = events.get()
    if type(event) != Events.Press:
        return None
    return key_to_char(event.key)


def key_to_char(key: Key) -> Optional[str]:
    if not hasattr(key, 'char'):
        return None
    return key.char


def on_release(key: Key):
    if context.get_game() == enums.GameState.RESTART and key_to_char(key) == enums.KeyCommand.RESTART:
        backspace()
        return False
    return True
