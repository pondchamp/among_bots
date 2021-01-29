import re
from typing import Optional, List

from controller.helpers import get_player_colour
from data import enums, params, consts
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
        if not self.game_state.game_started:
            return None
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

        players = {get_player_colour(p): p
                   for p in self.game_state.get_players(include_me=True)}
        aliases = {
            # Players
            "dark green": "green",
            "light green": "lime",
            "dark blue": "blue",
            "light blue": "cyan",
            "purp": "purple",
            "orang": "orange",
            "yallow": "yellow",

            # Locations
            "cafeteria": "caf",
            "coms": "comms",
            "navigation": "nav",
            "reac": "reactor",
            "medbay": "med bay",
            "elec": "electrical",
            "elect": "electrical",

            # Misspellings
            "imposter": "impostor",
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
        target_colours = []
        for colour in [p for p in players if p != player_colour]:
            p = players[colour]
            if p.name is False or p.color is False:
                continue
            name = p.name.decode("utf-8").strip()
            if name.lower() in ["i", "he", "she", "ok", "impostor", "imposter"] \
                    or len(name) == 0:  # pronoun and unhelpful names
                name = None
            if self._find(rf'\b{colour}\b') \
                    or (name is not None and self._find(rf'\b{name.lower()}\b')):
                target_colours.append(colour)
        if len(target_colours) == 0:  # Determine target implicitly
            if self._find(r"\b(self( report)?)\b"):
                target_colours.append(started_by)

        target_is_me = self.game_state.me_colour in target_colours
        verb = offset = None
        flags = []
        if len(target_colours) > 0:
            verb, offset = "mentioned", -0.5
            for target_colour in target_colours:
                if self._find(r"\b(sus|vent(ed)?|faked?|kill(ed)?|body|self report(ed)?|imp(ostor)?)\b") \
                        or self._find(rf"\b(vote|it'?s?) {target_colour}\b") \
                        or self._message_lower == target_colour:
                    verb, offset = "sussed", -1
                    break
                elif self._find(r"\b(safe|good|clear(ed)?)\b") \
                        or self._find(rf"\b(not|with|me and) {target_colour}\b") \
                        or self._find(rf"{target_colour} (and i|((had|did|has|do) )?(trash|chute|scan(ned)?|med))\b"):
                    verb, offset = "vouched for", 1
                    break
        if verb == "sussed" and target_is_me:
            if self._find(r"\b(vent(ed)?)\b"):
                flags.append(rF.ACCUSED_VENT)
        if verb:
            if self.player.alive and player_colour != UNKNOWN and len(context.trust_map) != 0:
                for target_colour in target_colours:
                    context.trust_map_score_offset(player_colour, target_colour, offset)
            print('>>', player_colour, verb, ', '.join(target_colours), '<<')
            if consts.debug_chat and len(flags) > 0:
                print('Adding flags:', flags)
            for f in flags: 
                context.response_flags_append(f)
        print(player_name, f'({player_colour}):', self.message)
        return self.message

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self._message_lower)) > 0

    def _find_all(self, pattern: str) -> List[str]:
        return re.findall(pattern, self._message_lower)
