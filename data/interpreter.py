import re
from typing import Optional

from controller.helpers import get_player_colour
from data import enums, params
from data.enums import ResponseFlags as rF
from state.game import GameState
from state.context import context
from lib.amongUsParser.gameEngine import PlayerClass

UNKNOWN = "unknown"


class Interpreter:
    def __init__(self, game_state: GameState, player: PlayerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self._message_lower = re.sub(r'[^\w\s?]', '', self.message.strip().lower())

    def interpret(self) -> Optional[str]:
        me = self.game_state.me
        if not me:
            print('Player info not loaded - please leave and rejoin the lobby.')
            return None
        if self.game_state.meeting_reason is False or self.player.playerId == me.playerId:
            return None

        player_name = self.player.name.decode("utf-8")
        player_colour: str = UNKNOWN
        if self.player.color is not False:
            player_colour = get_player_colour(self.player)
        if me.alive and not self.player.alive:
            print(player_name, f'({player_colour}): [DEAD CHAT HIDDEN]')
            return None

        target_name = target_colour = None
        target_is_me = False
        players = {get_player_colour(p): p
                   for p in self.game_state.get_players(include_me=True)}
        aliases = {
            # Players
            "purp": "purple",
            "orang": "orange",
            "dark green": "green",
            "light green": "lime",
            "dark blue": "blue",
            "light blue": "cyan",

            # Locations
            "cafeteria": "caf",
            "navigation": "nav",
            "reac": "reactor",
            "medbay": "med bay",

            # Misspellings
            "imposter": "impostor",
            "yallow": "yellow",
        }
        for k, v in aliases.items():
            self._message_lower = re.sub(rf'\b{k}\b', v, self._message_lower)

        # Check for locations
        curr_map = self.game_state.map
        started_by = self.game_state.get_player_colour_from_id(self.game_state.meeting_started_by.playerId) \
            if self.game_state.meeting_started_by else None
        if curr_map is not None and rF.BODY_NOT_LOCATED in self.game_state.get_response_flags() \
                and started_by == player_colour:
            for loc in params.location[enums.AUMap.COMMON] + params.location[curr_map]:
                if self._find(rf'\b{loc}\b'):
                    context.player_loc['body'] = loc
                    context.response_flags_remove(rF.BODY_NOT_LOCATED)
                    print("Location identified:", loc)

        # Check for names
        for colour in [p for p in players if p != player_colour]:
            p = players[colour]
            if p.name is False or p.color is False:
                continue
            name = p.name.decode("utf-8")
            if name.lower() in ["i", "he", "she", "ok", "impostor", "imposter"]:  # pronoun and unhelpful names
                name = None
            if self._find(rf'\b{colour}\b') \
                    or (name is not None and self._find(rf'\b{name.lower()}\b')):
                target_name = name
                target_colour = colour
                target_is_me = target_colour == self.game_state.me_colour
                break

        verb = offset = None
        flags = []
        if target_name is not None:
            verb, offset = "mentioned", -0.5
            if self._find(r"\b(sus|vent(ed)?|faked?|kill(ed)?|body|self report|imp(ostor)?)\b") \
                    or self._find(rf"\b(vote|it'?s?) {target_colour}\b") \
                    or self._message_lower == target_colour:
                verb, offset = "sussed", -1
            elif self._find(r"\b(safe|good|clear(ed)?)\b") \
                    or self._find(rf"\b(not|with|me and) {target_colour}\b") \
                    or self._find(rf"{target_colour} (and i|((had|did|has|do) )?(trash|chute|scan(ned)?|med))\b"):
                verb, offset = "vouched for", 1
        if verb == "sussed" and target_is_me:
            if self._find(r"\b(vent(ed)?)\b"):
                flags.append(rF.ACCUSED_VENT)
        if verb:
            if self.player.alive and player_colour != UNKNOWN and target_colour != UNKNOWN and \
                    len(context.trust_map) != 0:
                context.trust_map_score_offset(player_colour, target_colour, offset)
            target_label = "you" if target_is_me else target_colour
            print('>>', player_colour, verb, target_label, '<<')
            print('Adding flags:', flags)
            for f in flags: 
                context.response_flags_append(f)
        print(player_name, f'({player_colour}):', self.message)
        return self.message

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self._message_lower)) > 0
