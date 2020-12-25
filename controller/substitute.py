from typing import Dict, List

from data import params
from data.enums import AUMap, Substitution
from data.state import context


class SubstituteHelper:
    def __init__(self, players: List[str]):
        self.players = players if players is not None and len(players) > 0 else params.player
        last_seen = [p for p in context.get_last_seen() if p in self.players]
        last_seen = last_seen if len(last_seen) > 0 else context.get_last_seen()
        last_seen = last_seen if len(last_seen) > 0 else self.players
        self.substitutions: Dict[Substitution, Dict[AUMap, List[str]]] = {
            Substitution.PLAYER: {AUMap.COMMON: params.player},
            Substitution.PLAYER_NEAREST: {AUMap.COMMON: last_seen},
            Substitution.LOCATION: params.location,
            Substitution.LOCATION_ME: {AUMap.COMMON: [context.get_player_loc()['me']]},
            Substitution.LOCATION_BODY: {AUMap.COMMON: [context.get_player_loc()['body']]},
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
