# Kudos: https://github.com/jordam/amongUsParser
from data import enums
from data.enums import AUMap
from lib.amongUsParser.gameEngine import gameState, playerClass
from scapy.all import *
from scapy.layers.inet import UDP


def _get_player_colour(p: playerClass) -> enums.PlayerColour:
    return enums.PlayerColour.__call__(p.color)


class GameState(Thread):
    def __init__(self):
        self.game: gameState = gameState()  # No callbacks
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        sniff(prn=self.pkt_callback,
              filter="udp portrange 22023-22923",
              store=0)

    def pkt_callback(self, pkt):
        self.game.proc(pkt[UDP].payload.load, pkt.time)

    def get_me(self) -> Optional[str]:
        if self.game.selfClientID:
            me = self.game.players[self.game.selfClientID]
            return _get_player_colour(me).name
        return None

    def get_map(self) -> Optional[AUMap]:
        if self.game.gameSettings:
            au_map = self.game.gameSettings['MapId']
            return enums.AUMap.__call__(au_map)
        return None

    def get_impostor_count(self) -> Optional[int]:
        if self.game.gameSettings:
            return self.game.gameSettings['NumImpostors']
        return None

    def get_players(self) -> Optional[List[str]]:
        if self.game.players:
            return [_get_player_colour(p).name.lower() for p in self.game.players.values()]
        return None
