import re
from data import enums
from lib.amongUsParser.gameEngine import playerClass

class Interpreter:
    def __init__(self, game_state, player: playerClass, message: str):
        self.game_state = game_state
        self.player = player
        self.message = message
        self.message_lower =  re.sub(r'[^\w\s]', '', self.message.lower())

    def interpret(self) -> str:
        me = self.game_state.get_me()
        if not me:
            print('Player info not loaded - please leave and rejoin the lobby.')
            return self.message
        player_name = self.player.name.decode("utf-8")
        my_message = self.player.playerId == me.playerId
        player_id = 'me' if my_message else self.player.playerId
        verb = None
        if not my_message:
            me_colour: enums.PlayerColour = enums.PlayerColour.__call__(me.color)
            me_name = me.name.decode("utf-8")
            if self._find(me_colour.name.lower()) \
                    or self._find(me_name.lower()):
                verb = "mentioned"
                if self._find("sus"):
                    verb = "sussed"
        if verb:
            print('>>', player_name, verb, "you!", '<<')

        return f'{player_name} ({player_id}): {self.message}'

    def _find(self, pattern) -> bool:
        return len(re.findall(pattern, self.message_lower)) > 0