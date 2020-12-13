from typing import Optional, List
import datetime

from data.sus_score import PlayerSus


class Context:
    def __init__(self):
        self._state_debug: bool = False
        self._state_capture_keys: bool = False
        self._state_chat_turns: int = 0
        self._state_chat_log: List[str] = []
        self._state_last_phrase: Optional[str] = None
        self._state_last_response: Optional[datetime.datetime] = None
        self._state_player_sus: Optional[List[PlayerSus]] = None

    def get_debug(self) -> bool:
        return self._state_debug

    def set_debug(self, val: bool):
        self._state_debug = val

    def get_capture_keys(self) -> bool:
        return self._state_capture_keys

    def set_capture_keys(self, val: bool):
        self._state_capture_keys = val

    def get_chat_turns(self) -> int:
        return self._state_chat_turns

    def get_chat_log(self) -> List[str]:
        return self._state_chat_log

    def chat_log_append(self, val: str):
        self._state_chat_turns += 1
        self._state_chat_log.append(val)

    def chat_log_clear(self):
        self._state_chat_log = []

    def chat_log_reset(self):
        self.chat_log_clear()
        self._state_chat_turns = 0

    def get_last_response(self) -> Optional[datetime.datetime]:
        return self._state_last_response

    def set_last_response(self, val: Optional[datetime.datetime]):
        self._state_last_response = val

    def get_last_phrase(self) -> Optional[str]:
        return self._state_last_phrase

    def set_last_phrase(self, val: Optional[str]):
        self._state_last_phrase = val

    def get_player_sus(self) -> Optional[List[PlayerSus]]:
        return self._state_player_sus

    def set_player_sus(self, val: Optional[List[PlayerSus]]):
        self._state_player_sus = val


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
