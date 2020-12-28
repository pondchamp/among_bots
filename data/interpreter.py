import re
from typing import Optional, Dict

from controller.helpers import get_player_colour
from data import enums
from state.game import GameState
from state.context import context
from lib.amongUsParser.gameEngine import PlayerClass


class Interpreter:
    def __init__(self, game_state: GameState, player: PlayerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self._message_lower = re.sub(r'[^\w\s?]', '', self.message.strip().lower())

    def interpret(self) -> Optional[str]:
        me = self.game_state.me
        if not me:
            print('Player info not loaded.')
            return None
        if not self.game_state.game_started or self.player.playerId == me.playerId:
            return None

        player_name = self.player.name.decode("utf-8")
        player_colour: str = 'Unknown'
        if self.player.color is not False:
            player_colour = get_player_colour(self.player)
        if me.alive and not self.player.alive:
            print(player_name, f'({player_colour}): [DEAD CHAT HIDDEN]')
            return None

        target_name = target_colour = None
        players = {get_player_colour(p): p
                   for p in self.game_state.get_players(include_me=True)}
        aliases = {
            "purp": "purple",
            "orang": "orange",
            "dark green": "green",
            "light green": "lime",
            "dark blue": "blue",
            "light blue": "cyan",
        }
        for k, v in aliases.items():
            self._message_lower = re.sub(rf'\b{k}\b', v, self._message_lower)
        for alias in [p for p in sorted(players.keys(), reverse=True) if p != player_colour]:
            p = players[alias]
            alias = str(alias).removeprefix('~')
            if p.name is False or p.color is False:
                continue
            name = p.name.decode("utf-8")
            if name.lower() in ["i", "he", "she", "ok"]:  # pronoun and unhelpful names
                name = None
            colour = enums.PlayerColour.__call__(p.color)
            if self._find(rf'\b{alias}\b') \
                    or (name is not None and self._find(rf'\b{name.lower()}\b')):
                target_name = name
                target_colour = colour
                break

        verb = offset = None
        if target_name is not None:
            verb, offset = "mentioned", -0.5
            t_col = target_colour.name.lower()
            if self._find(r"\b(sus|vent(ed)?|faked?|kill(ed)?|body|self report)\b") \
                    or self._find(rf"\b(vote|it'?s?) {t_col}\b") \
                    or self._message_lower == t_col:
                verb, offset = "sussed", -1
            elif self._find(r"\b(safe|good|clear(ed)?)\b") \
                    or self._find(rf"\b(not|with|me and) {t_col}\b") \
                    or self._find(rf"{t_col} (and i|((had|did|has|do) )?(trash|chute|scan|med))\b"):
                verb, offset = "vouched for", 1
        if verb:
            if self.player.alive and player_colour != 'Unknown' and target_colour != 'Unknown' and \
                    len(context.trust_map) != 0:
                context.trust_map_score_offset(player_colour, target_colour.name.lower(), offset)
            print('>>', player_colour, verb, target_colour.name.lower(), "!", '<<')
        print(player_name, f'({player_colour}):', self.message)
        return self.message

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self._message_lower)) > 0
