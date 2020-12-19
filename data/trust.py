from typing import List


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
                for p2 in players:
                    self._map[p1][p2] = 0
        else:  # update
            for p1 in self._map.copy().keys():
                if p1 not in players:
                    del self._map[p1]
                    continue
                for p2 in self._map[p1].copy().keys():
                    if p2 not in players:
                        del self._map[p1][p2]

    def update_score(self, p1: str, p2: str, score: int):
        self._map[p1][p2] = score
