import re
from typing import Optional

from data import enums
from data.state import context
from lib.amongUsParser.gameEngine import PlayerClass


class Interpreter:
    def __init__(self, game_state, player: PlayerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self.message_lower = re.sub(r'[^\w\s?]', '', self.message.strip().lower())

    def interpret(self) -> Optional[str]:
        me = self.game_state.get_me()
        if not me:
            print('Player info not loaded.')
            return None
        if not self.game_state.get_game_started() or self.player.playerId == me.playerId:
            return None

        player_name = self.player.name.decode("utf-8")
        player_colour: str = 'Unknown'
        if self.player.color is not False:
            player_colour = enums.PlayerColour.__call__(self.player.color).name.lower()
        if me.alive and not self.player.alive:
            return f'{player_name} ({player_colour}): [DEAD CHAT HIDDEN]'

        target_name = target_colour = None
        players = {enums.PlayerColour.__call__(p.color).name.lower(): p
                   for p in self.game_state.get_players(include_me=True)}
        if "purple" in players:
            players["purp"] = players["purple"]
        for alias in players:
            p = players[alias]
            if not p.name or not p.color:
                continue
            name = p.name.decode("utf-8")
            colour = enums.PlayerColour.__call__(p.color)
            if self._find(rf'\b{alias}\b') \
                    or self._find(name.lower()):
                target_name = name
                target_colour = colour
                break

        offset = None
        verb = None
        if target_name is not None:
            verb = "mentioned"
            offset = -0.5
            if self._find(r"\b(sus|vote|vent|it'?s?|faked?|kill(ed)?)\b") or self.message_lower == target_colour.name.lower():
                verb = "sussed"
                offset = -1
            elif self._find(r"\b(safe|not|good|clear(ed)?|with)\b"):
                verb = "vouched for"
                offset = 1
        if verb:
            if me.alive and player_colour != 'Unknown' and target_colour != 'Unknown' and \
                    len(context.get_trust_map()) != 0:
                context.trust_map_score_offset(player_colour, target_colour.name.lower(), offset)
            print('>>', player_colour, verb, target_colour.name.lower(), "!", '<<')
        return f'{player_name} ({player_colour}): {self.message}'

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self.message_lower)) > 0
