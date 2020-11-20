from typing import List

from data import params
from data.enums import AUMap


class Substitutions:
    def __init__(self, players: List[str]):
        self.players = players
        self.substitutions = {
            "p": params.player,
            "l": params.location,
            "t": params.task
        }

    def get(self, curr_map: 'AUMap', key: str) -> List[str]:
        if key == "p" and self.players is not None:
            return self.players
        if key in ["l", "t"]:
            subs = self.substitutions[key]
            maps = subs[-1] + subs[curr_map]
            return maps
        return self.substitutions[key]
