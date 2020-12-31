import time
from typing import Optional
from pynput.keyboard import Controller, Key, Events, Listener
from win32api import GetKeyState
from win32con import VK_CAPITAL

keyboard_controller = Controller()


def new_listener() -> Listener:
    return Listener()


def caps_enabled() -> bool:
    return bool(GetKeyState(VK_CAPITAL))


def write_text(text: str):
    for key in text:
        time.sleep(0.01)
        press(key)
    time.sleep(0.1)
    press(Key.enter)


def backspace():
    press(Key.backspace)


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


def press(key: Key):
    keyboard_controller.press(key)
    keyboard_controller.release(key)
