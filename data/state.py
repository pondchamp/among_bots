from contextvars import ContextVar
from typing import List, Optional

from data import enums


class Context:
    def __init__(self):
        self._capture_keys: ContextVar[bool] = ContextVar("capture_keys", default=False)
        self._state_me: ContextVar[Optional[str]] = ContextVar("state_me", default=None)
        self._state_players: ContextVar[Optional[List[str]]] = ContextVar("state_players", default=None)
        self._state_map: ContextVar[Optional[enums.AUMap]] = ContextVar("state_map", default=None)
        self._state_game: ContextVar[enums.GameState] = ContextVar("state_game", default=enums.GameState.SETUP)

    def get_capture_keys(self) -> bool:
        val = self._capture_keys.get()
        return bool(val)

    def set_capture_keys(self, val: bool):
        self._capture_keys.set(val)

    def get_state_me(self) -> Optional[str]:
        val = self._state_me.get()
        return str(val)

    def set_state_me(self, val: Optional[str]):
        self._state_me.set(val)

    def get_state_players(self) -> Optional[List[str]]:
        val = self._state_players.get()
        if val is None:
            return None
        return list(val)

    def set_state_players(self, val: Optional[List[str]]):
        self._state_players.set(val)

    def get_state_map(self) -> Optional[enums.AUMap]:
        val = self._state_map.get()
        return enums.AUMap.__call__(val)

    def set_state_map(self, val: Optional[enums.AUMap]):
        self._state_map.set(val)

    def get_state_game(self) -> enums.GameState:
        val = self._state_game.get()
        return enums.GameState.__call__(val)

    def set_state_game(self, val: enums.GameState):
        self._state_game.set(val)


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
