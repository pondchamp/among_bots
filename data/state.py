from contextvars import ContextVar
from typing import List, Optional
import datetime

from data import enums
from data.sus_score import PlayerSus


class Context:
    def __init__(self):
        self._state_capture_keys: ContextVar[bool] = ContextVar("capture_keys", default=False)
        self._state_me: ContextVar[Optional[str]] = ContextVar("state_me", default=None)
        self._state_players: ContextVar[Optional[List[PlayerSus]]] = ContextVar("state_players", default=None)
        self._state_map: ContextVar[Optional[enums.AUMap]] = ContextVar("state_map", default=None)
        self._state_last_response: ContextVar[Optional[datetime.datetime]] = ContextVar("last_response", default=None)
        self._state_num_impostor: ContextVar[int] = ContextVar("num_impostor", default=1)

    def get_capture_keys(self) -> bool:
        val = self._state_capture_keys.get()
        return val

    def set_capture_keys(self, val: bool):
        self._state_capture_keys.set(val)

    def get_me(self) -> Optional[str]:
        val = self._state_me.get()
        return val

    def set_me(self, val: Optional[str]):
        self._state_me.set(val)

    def get_players(self) -> Optional[List[PlayerSus]]:
        val = self._state_players.get()
        return val

    def set_players(self, val: Optional[List[PlayerSus]]):
        self._state_players.set(val)

    def get_map(self) -> Optional[enums.AUMap]:
        val = self._state_map.get()
        return enums.AUMap.__call__(val)

    def set_map(self, val: Optional[enums.AUMap]):
        self._state_map.set(val)

    def get_last_response(self) -> Optional[datetime.datetime]:
        val = self._state_last_response.get()
        return val

    def set_last_response(self, val: Optional[datetime.datetime]):
        self._state_last_response.set(val)

    def get_num_impostor(self) -> int:
        val = self._state_num_impostor.get()
        return val

    def set_num_impostor(self, val: int):
        self._state_num_impostor.set(val)


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
