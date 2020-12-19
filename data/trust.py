from enum import Enum
from typing import List, Dict


class SusScore(Enum):
    SUS = -1.0
    SAFE = 1.0


class TrustMap:
    def __init__(self):
        self._map = {}

    def get_map(self):
        return self._map

    def update_players(self, players: List[str]):
        if players is None or len(players) == 0:  # reset
            self._map = {}
            return
        if len(self._map) == 0:  # initialise
            for p1 in players:
                self._map[p1] = {}
        else:  # update
            for p1 in self._map.copy().keys():
                if p1 not in players:
                    del self._map[p1]
                    continue
                for p2 in self._map[p1].copy().keys():
                    if p2 not in players:
                        del self._map[p1][p2]

    def update_score(self, p1: str, p2: str, score: float):
        if p2 not in self._map[p1]:
            self._map[p1][p2] = 0
        self._map[p1][p2] = score

    def offset_score(self, p1: str, p2: str, offset: float):
        if p2 not in self._map[p1]:
            self._map[p1][p2] = 0
        self._map[p1][p2] += offset

    def aggregate_scores(self) -> Dict[str, float]:
        out = {x: 0.0 for x in self._map.keys()}
        max_abs = 0.0
        for p1 in self._map.keys():
            for p2 in self._map[p1].keys():
                out[p2] += self._map[p1][p2]
        for p in out:
            max_abs = max(max_abs, abs(out[p]))
        if max_abs != 0.0 and max_abs != 1.0:
            for p in out:
                out[p] /= max_abs
        return out

    def scale_scores(self, ratio: float):
        for p1 in self._map.keys():
            for p2 in self._map[p1].keys():
                self._map[p1][p2] *= ratio
