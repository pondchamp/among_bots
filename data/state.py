from contextvars import ContextVar
from typing import List, Optional
import datetime

from data import enums


class Context:
    def __init__(self):
        self._state_capture_keys: ContextVar[bool] = ContextVar("capture_keys", default=False)
        self._state_me: ContextVar[Optional[str]] = ContextVar("state_me", default=None)
        self._state_players: ContextVar[Optional[List[str]]] = ContextVar("state_players", default=None)
        self._state_map: ContextVar[Optional[enums.AUMap]] = ContextVar("state_map", default=None)
        self._state_game: ContextVar[enums.GameState] = ContextVar("state_game", default=enums.GameState.SETUP)
        self._state_last_response: ContextVar[Optional[datetime.datetime]] = ContextVar("last_response", default=None)

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

    def get_players(self) -> Optional[List[str]]:
        val = self._state_players.get()
        return val

    def set_players(self, val: Optional[List[str]]):
        self._state_players.set(val)

    def get_map(self) -> Optional[enums.AUMap]:
        val = self._state_map.get()
        return enums.AUMap.__call__(val)

    def set_map(self, val: Optional[enums.AUMap]):
        self._state_map.set(val)

    def get_game(self) -> enums.GameState:
        val = self._state_game.get()
        return enums.GameState.__call__(val)

    def set_game(self, val: enums.GameState):
        self._state_game.set(val)

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
