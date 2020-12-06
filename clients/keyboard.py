import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener

from data import enums
from data.state import context

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener()


def handle_key(key: str) -> Optional[enums.KeyCommand]:
    capture_keys = context.get_capture_keys()

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
                print_commands()
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
    if hasattr(key, 'char'):
        return key.char
    elif hasattr(key, 'name'):
        return key.name
    return None


def print_commands():
    print("COMMANDS")
    for x in [x for x in enums.KeyCommand if x != enums.KeyCommand.KEY_CAP]:
        k = str.upper(x.value)
        v = str.title(x.name).replace('_', ' ')
        current = None
        print(f'{k}: {v}{f" (Current: {str(current).title()})" if current is not None else ""}')
