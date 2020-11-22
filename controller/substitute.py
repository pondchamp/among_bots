from typing import Dict, List

from data import params
from data.enums import AUMap, Substitution


class SubstituteHelper:
    def __init__(self, players: List[str]):
        self.players = players if players is not None and len(players) > 0 else params.player
        self.substitutions: Dict[Substitution, Dict[AUMap, List[str]]] = {
            Substitution.PLAYER: {AUMap.COMMON: params.player},
            Substitution.LOCATION: params.location,
            Substitution.TASK: params.task
        }

    def get(self, curr_map: AUMap, key: Substitution) -> List[str]:
        if key == Substitution.PLAYER and self.players is not None:
            return self.players
        if key in [Substitution.LOCATION, Substitution.TASK]:
            subs = self.substitutions[key]
            maps = subs[AUMap.COMMON] + subs[curr_map]
            return maps
        return self.substitutions[key][AUMap.COMMON]
