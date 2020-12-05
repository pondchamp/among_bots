from contextvars import ContextVar
from typing import List, Tuple, Optional
import datetime


class Context:
    def __init__(self):
        self._state_capture_keys: ContextVar[bool] = ContextVar("capture_keys", default=False)

        self._state_is_impostor: ContextVar[Tuple[bool, Optional[List[str]]]] = \
            ContextVar("is_impostor", default=(False, None))
        self._state_chat_turns: ContextVar[int] = ContextVar("chat_turns", default=0)

        self._state_last_response: ContextVar[Optional[datetime.datetime]] = ContextVar("last_response", default=None)

    def get_capture_keys(self) -> bool:
        val = self._state_capture_keys.get()
        return val

    def set_capture_keys(self, val: bool):
        self._state_capture_keys.set(val)

    def get_is_impostor(self) -> Tuple[bool, Optional[List[str]]]:
        val = self._state_is_impostor.get()
        return val

    def set_is_impostor(self, val: Tuple[bool, Optional[List[str]]]):
        self._state_is_impostor.set(val)

    def get_chat_turns(self) -> int:
        val = self._state_chat_turns.get()
        return val

    def set_chat_turns(self, val: int):
        self._state_chat_turns.set(val)

    def get_last_response(self) -> Optional[datetime.datetime]:
        val = self._state_last_response.get()
        return val

    def set_last_response(self, val: Optional[datetime.datetime]):
        self._state_last_response.set(val)


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
