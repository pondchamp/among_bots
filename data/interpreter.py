import re
from typing import Optional

from data import enums, consts
from data.state import context
from lib.amongUsParser.gameEngine import PlayerClass


class Interpreter:
    def __init__(self, game_state, player: PlayerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self.message_lower = re.sub(r'[^\w\s]', '', self.message.strip().lower())

    def interpret(self) -> Optional[str]:
        me = self.game_state.get_me()
        if not me:
            print('Player info not loaded.')
            return self.message
        if not self.game_state.get_game_started() or self.player.playerId == me.playerId:
            return None
        if me.alive and not self.player.alive:
            self.message = '[DEAD CHAT HIDDEN]'

        player_name = self.player.name.decode("utf-8")
        player_colour: str = 'Unknown'
        if self.player.color:
            player_colour = enums.PlayerColour.__call__(self.player.color).name.lower()
        if not me.name:
            print('Self info not loaded.')
            return self.message

        target_name = target_colour = None
        for p in self.game_state.get_players(include_me=True):
            name = p.name.decode("utf-8")
            colour = enums.PlayerColour.__call__(p.color)
            if self._find(rf'\b{colour.name.lower()}\b') \
                    or self._find(name.lower()):
                target_name = name
                target_colour = colour
                break

        offset = None
        verb = None
        if target_name is not None:
            verb = "mentioned"
            offset = -0.5
            if self._find("sus|vote|vent|it'?s?") or self.message_lower == target_colour.name.lower():
                verb = "sussed"
                offset = -1
            elif self._find("safe|not"):
                verb = "vouched for"
                offset = 1
        if verb:
            context.trust_map_score_offset(player_colour, target_colour.name.lower(), offset)
            print('>>', player_name, verb, target_name, "!", '<<')
            if consts.debug_chat:
                print("Trust map:")
                for x in context.get_trust_map():
                    print(x, "\t:", context.get_trust_map()[x])

        return f'{player_name} ({player_colour}): {self.message}'

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self.message_lower)) > 0
