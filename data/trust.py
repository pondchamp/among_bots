import math
from enum import Enum
from typing import List, Dict, Optional


class SusScore(Enum):
    SUS = -1.0
    SAFE = 1.0


class TrustMap:
    def __init__(self, trust_max=1.0):
        self._map = {}
        if trust_max < 0:
            raise ValueError('trust_max must be non-negative')
        self.trust_max = trust_max

    @property
    def map(self):
        return self._map

    @property
    def players(self) -> List[str]:
        return [p for p in self._map]

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
        self._map[p1][p2] = self._min_sign(score, self.trust_max)

    def offset_score(self, p1: str, p2: str, offset: float):
        if p1 not in self._map:
            return
        if p2 not in self._map[p1]:
            self._map[p1][p2] = 0
        self._map[p1][p2] += offset
        self._map[p1][p2] = self._min_sign(self._map[p1][p2], self.trust_max)

    def aggregate_scores(self, me: Optional[str] = None) -> Dict[str, float]:
        out = {x: 0.0 for x in self._map.keys()}
        max_abs = 0.0
        for p1 in self._map.keys():
            for p2 in self._map[p1].keys():
                out[p2] += self._map[p1][p2]
        if me is not None and me in out:
            del out[me]
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

    @staticmethod
    def _min_sign(a_signed: float, b_unsigned: float) -> float:
        if b_unsigned < 0:
            raise ValueError('b_unsigned must be non-negative')
        sign = math.copysign(1, a_signed)
        a_unsigned = abs(a_signed)
        return min(a_unsigned, b_unsigned) * sign
