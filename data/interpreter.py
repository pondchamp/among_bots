import re
from data import enums
from lib.amongUsParser.gameEngine import playerClass


class Interpreter:
    def __init__(self, game_state, player: playerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self.message_lower = re.sub(r'[^\w\s]', '', self.message.lower())

    def interpret(self) -> str:
        me = self.game_state.get_me()
        if not me:
            print('Player info not loaded - please leave and rejoin the lobby.')
            return self.message
        if self.player.playerId == me.playerId:
            return self.message
        if me.alive and not self.player.alive:
            self.message = '[DEAD CHAT HIDDEN]'

        player_name = self.player.name.decode("utf-8")
        player_colour: enums.PlayerColour = enums.PlayerColour.__call__(self.player.color).name
        me_name = me.name.decode("utf-8")
        me_colour: enums.PlayerColour = enums.PlayerColour.__call__(me.color)

        verb = None
        if self._find(me_colour.name.lower()) \
                or self._find(me_name.lower()):
            verb = "mentioned"
            if self._find("sus"):
                verb = "sussed"
            elif self._find("safe"):
                verb = "vouched for"
        if verb:
            print('>>', player_name, verb, "you!", '<<')

        return f'{player_name} ({player_colour}): {self.message}'

    def _find(self, pattern: str) -> bool:
        return len(re.findall(pattern, self.message_lower)) > 0
