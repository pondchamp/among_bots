from typing import Optional, List, Dict
import datetime

from data.sus_score import PlayerSus
from data.trust import TrustMap


class Context:
    def __init__(self):
        self._state_debug: bool = False
        self._state_capture_keys: bool = True
        self._state_chat_turns: int = 0
        self._state_chat_log: List[str] = []
        self._state_last_phrase: Optional[str] = None
        self._state_last_response: Optional[datetime.datetime] = None
        self._state_player_sus: Optional[List[PlayerSus]] = None
        self._state_player_loc: Optional[Dict[str, str]] = None
        self._state_trust_map: TrustMap = TrustMap()

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

    def get_player_loc(self) -> Optional[Dict[str, str]]:
        return self._state_player_loc

    def set_player_loc(self, val: Optional[Dict[str, str]]):
        self._state_player_loc = val

    def get_trust_map(self) -> Dict:
        return self._state_trust_map.get_map()

    def set_trust_map_players(self, players: List[str]):
        self._state_trust_map.update_players(players)

    def reset_trust_map_players(self):
        self._state_trust_map.update_players([])

    def set_trust_map_score(self, p1: str, p2: str, score: int):
        self._state_trust_map.update_score(p1, p2, score)


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
