import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener
from win32api import GetKeyState
from win32con import VK_CAPITAL

from data import enums
from data.state import context

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener()


def caps_enabled() -> bool:
    return bool(GetKeyState(VK_CAPITAL))


def handle_key(key: str) -> Optional[enums.KeyCommand]:
    mode = enums.get_key_command(key)
    if mode is None:
        return None

    if context.capture_keys or mode == enums.KeyCommand.KEY_CAP:
        backspace()
        if mode == enums.KeyCommand.KEY_CAP:
            context.capture_keys = not context.capture_keys
            print("KEY CAPTURE", "ENABLED" if context.capture_keys else "DISABLED")
            if context.capture_keys:
                print_commands()
        else:
            return mode


def write_text(text: str):
    for key in text:
        time.sleep(0.02)
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
        print(f'{k}\t:', v)
    print()
