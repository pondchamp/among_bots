import re
from typing import Optional, Dict

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
            print(player_name, f'({player_colour}): [DEAD CHAT HIDDEN]')
            return None

        target_name = target_colour = None
        players = {enums.PlayerColour.__call__(p.color).name.lower(): p
                   for p in self.game_state.get_players(include_me=True)}
        self._alias(players, "purple", "~purp")
        self._alias(players, "orange", "~orang")
        self._alias(players, "green", "~dark green")
        self._alias(players, "lime", "~light green")
        self._alias(players, "blue", "~dark blue")
        self._alias(players, "cyan", "~light blue")
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
            if self._find(r"\b(sus|vent(ed)?|faked?|kill(ed)?|body|self report)\b") or \
                    self._find(rf"\b(vote|it'?s?) {t_col}\b") or self.message_lower == t_col:
                verb, offset = "sussed", -1
            elif self._find(r"\b(safe|good|clear(ed)?)\b") or self._find(rf"\b(not|with|me and) {t_col}\b") or \
                    self._find(rf"{t_col} (and i|((had|did|has|do) )?(trash|chute|scan|med))\b"):
                verb, offset = "vouched for", 1
        if verb:
            if self.player.alive and player_colour != 'Unknown' and target_colour != 'Unknown' and \
                    len(context.get_trust_map()) != 0:
                context.trust_map_score_offset(player_colour, target_colour.name.lower(), offset)
            print('>>', player_colour, verb, target_colour.name.lower(), "!", '<<')
        print(player_name, f'({player_colour}):', self.message)
        return self.message

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self.message_lower)) > 0

    @staticmethod
    def _alias(players: Dict, colour: str, alias: str):
        if colour in players:
            players[alias] = players[colour]
