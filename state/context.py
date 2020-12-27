import os
import pickle
from typing import Optional, List, Dict
import datetime

from data.trust import TrustMap


class Context:
    def __init__(self):
        self._state_use_gcp: bool = False
        self._state_debug: bool = False
        self._state_capture_keys: bool = True

        self._state_chat_turns: int = 0
        self._state_chat_log: List[str] = []
        self._state_last_phrase: Optional[str] = None
        self._state_last_response: Optional[datetime.datetime] = None
        self._state_player_loc: Optional[Dict[str, str]] = None
        self._state_trust_map: TrustMap = TrustMap()
        self._state_last_seen: List[str] = []

    @property
    def use_gcp(self) -> bool:
        return self._state_use_gcp

    @use_gcp.setter
    def use_gcp(self, val: bool):
        self._state_use_gcp = val

    @property
    def debug(self) -> bool:
        return self._state_debug

    @debug.setter
    def debug(self, val: bool):
        self._state_debug = val

    @property
    def capture_keys(self) -> bool:
        return self._state_capture_keys

    @capture_keys.setter
    def capture_keys(self, val: bool):
        self._state_capture_keys = val

    @property
    def chat_turns(self) -> int:
        return self._state_chat_turns

    @property
    def chat_log(self) -> List[str]:
        return self._state_chat_log

    def chat_log_append(self, val: str):
        self._state_chat_turns += 1
        self._state_chat_log.append(val)

    def chat_log_clear(self):
        self._state_chat_log = []

    def chat_log_reset(self):
        self.chat_log_clear()
        self._state_chat_turns = 0

    @property
    def last_response(self) -> Optional[datetime.datetime]:
        return self._state_last_response

    @last_response.setter
    def last_response(self, val: Optional[datetime.datetime]):
        self._state_last_response = val

    @property
    def last_phrase(self) -> Optional[str]:
        return self._state_last_phrase

    @last_phrase.setter
    def last_phrase(self, val: Optional[str]):
        self._state_last_phrase = val

    @property
    def player_loc(self) -> Optional[Dict[str, str]]:
        return self._state_player_loc

    @player_loc.setter
    def player_loc(self, val: Optional[Dict[str, str]]):
        self._state_player_loc = val

    @property
    def trust_map(self) -> Dict:
        return self._state_trust_map.map

    def trust_map_players_set(self, players: List[str]):
        self._state_trust_map.update_players(players)

    def trust_map_players_reset(self):
        self._state_trust_map.update_players([])

    def trust_map_player_remove(self, player: str):
        players = self._state_trust_map.players
        if player in players:
            players.remove(player)
            self._state_trust_map.update_players(players)

    def trust_map_score_get(self, me: Optional[str] = None) -> Dict[str, float]:
        return self._state_trust_map.aggregate_scores(me)

    def trust_map_score_offset(self, p1: str, p2: str, offset: float):
        self._state_trust_map.offset_score(p1, p2, offset)

    def trust_map_score_set(self, p1: str, p2: str, score: float):
        self._state_trust_map.update_score(p1, p2, score)

    def trust_map_score_scale(self, ratio: float):
        self._state_trust_map.scale_scores(ratio)

    @property
    def last_seen(self) -> List[str]:
        return self._state_last_seen.copy()

    def last_seen_append(self, val: str):
        self._state_last_seen.append(val)

    def last_seen_remove(self, val: str):
        self._state_last_seen.remove(val)

    def last_seen_reset(self):
        self._state_last_seen = []

    def update_state(self, game_state, root_dir: str):  # Untyped due to circular reference
        game_id = game_state.game_id
        if game_id is None:
            return
        file_path = root_dir + '\\' + str(game_id) + "_ctx"
        if game_state.curr_lobby != game_id and os.path.exists(file_path):
            with open(file_path, "rb") as fp:
                try:
                    state: Context = pickle.load(fp)
                except EOFError:
                    return
            self._update_state(state)
            with open(file_path, "wb") as fp:
                pickle.dump(state, fp)
        else:
            with open(file_path, "wb") as fp:
                pickle.dump(self, fp)

    def _update_state(self, state):
        self._state_chat_turns = state.chat_turns
        self._state_chat_log = state.chat_log
        self._state_last_phrase = state.last_phrase
        self._state_last_response = state.last_response
        self._state_player_loc = state.player_loc
        self._state_trust_map = state.trust_map
        self._state_last_seen = state.last_seen


context: Context = Context()
