import random
from typing import Optional, List, Dict
import datetime

from data import consts
from data.enums import ResponseFlags
from data.trust import TrustMap, SusScore


class Context:
    def __init__(self):
        self._state_debug: bool = False
        self._state_capture_keys: bool = True
        self._state_chat_turns: int = 0
        self._state_chat_log: List[str] = []
        self._state_last_phrase: Optional[str] = None
        self._state_last_response: Optional[datetime.datetime] = None
        self._state_player_loc: Optional[Dict[str, str]] = None
        self._state_trust_map: TrustMap = TrustMap()
        self._state_last_seen: List[str] = []

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

    def get_player_loc(self) -> Optional[Dict[str, str]]:
        return self._state_player_loc

    def set_player_loc(self, val: Optional[Dict[str, str]]):
        self._state_player_loc = val

    def get_trust_map(self) -> Dict:
        return self._state_trust_map.get_map()

    def trust_map_players_set(self, players: List[str]):
        self._state_trust_map.update_players(players)

    def trust_map_player_remove(self, player: str):
        players = self._state_trust_map.get_players()
        if player in players:
            players.remove(player)
            self._state_trust_map.update_players(players)

    def trust_map_players_reset(self):
        self._state_trust_map.update_players([])

    def trust_map_score_offset(self, p1: str, p2: str, offset: float):
        self._state_trust_map.offset_score(p1, p2, offset)

    def trust_map_score_set(self, p1: str, p2: str, score: float):
        self._state_trust_map.update_score(p1, p2, score)

    def trust_map_score_scale(self, ratio: float):
        self._state_trust_map.scale_scores(ratio)

    def trust_map_score_get(self, me=None) -> Dict[str, float]:
        return self._state_trust_map.aggregate_scores(me)

    def get_last_seen(self) -> List[str]:
        return self._state_last_seen.copy()

    def append_last_seen(self, val: str):
        self._state_last_seen.append(val)

    def remove_last_seen(self, val: str):
        self._state_last_seen.remove(val)

    def reset_last_seen(self):
        self._state_last_seen = []


def get_response_flags(game_state) -> List[ResponseFlags]:
    flags = []
    me = game_state.get_me()
    reason = game_state.get_meeting_reason()
    start_by = game_state.get_meeting_started_by()
    if random.random() < consts.SELF_SABOTAGE_PROB:
        flags.append(ResponseFlags.SELF_SABOTAGE)
    if me is not None and me.infected:
        flags.append(ResponseFlags.SELF_IMPOSTOR)
    if reason is not False and start_by is not False:
        if reason == 'Button':
            if me and start_by.playerId == me.playerId:
                flags.append(ResponseFlags.EMERGENCY_MEET_ME)
            else:
                flags.append(ResponseFlags.EMERGENCY_MEET_OTHER)
        else:  # Body found
            if me and start_by.playerId == me.playerId:
                flags.append(ResponseFlags.BODY_FOUND_ME)
            else:
                flags.append(ResponseFlags.BODY_FOUND_OTHER)
                player_colour = game_state.get_player_colour_from_id(start_by.playerId)
                trust_scores = context.trust_map_score_get()
                if player_colour in [p for p in trust_scores if trust_scores[p] == SusScore.SUS.value]:
                    flags.append(ResponseFlags.SELF_REPORT)

    return flags


context: Optional[Context] = None


def init():
    global context
    context = Context()


init()
