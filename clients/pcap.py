# Kudos: https://github.com/jordam/amongUsParser
from lib.amongUsParser.gameEngine import gameState, playerClass
from scapy.all import *
from scapy.layers.inet import UDP

from data import enums
from data.state import context
from data.sus_score import PlayerSus, SCORE_SUS, SCORE_SAFE


def _get_player_colour(p: playerClass) -> str:
    return enums.PlayerColour.__call__(p.color).name.lower()


class GameState(Thread):
    def __init__(self):
        self.game: gameState = gameState({
            'StartMeeting': self.start_meeting_callback
        })
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        sniff(prn=self.pkt_callback,
              filter="udp portrange 22023-22923",
              store=0)

    def pkt_callback(self, pkt):
        self.game.proc(pkt[UDP].payload.load, pkt.time)

    def get_me(self) -> Optional[playerClass]:
        return self.game.players[self.game.selfClientID] if self.game.selfClientID else None

    def get_me_colour(self) -> Optional[str]:
        me = self.get_me()
        return _get_player_colour(me) if me else None

    def get_map(self) -> Optional[enums.AUMap]:
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
            return [_get_player_colour(p) for p in self.game.players.values()
                    if p.alive and p.playerId != self.get_me().playerId]
        return None

    def get_is_impostor(self) -> Optional[bool]:
        me = self.get_me()
        return me.infected if me else None

    def get_impostor_list(self) -> Optional[List[str]]:
        if self.get_is_impostor() and self.game.players:  # Only show if I'm impostor (no cheating!)
            return [_get_player_colour(p) for p in self.game.players.values()
                    if p.infected and p.playerId != self.get_me().playerId]

    def start_meeting_callback(self, _):
        context.set_chat_turns(0)
        self.set_player_sus()

    def set_player_sus(self):
        players = self.get_players()
        if players is not None and len(players) > 0:
            players_score: List[PlayerSus] = []

            # Pick safe player/s
            imp_list = self.get_impostor_list()
            for i in ([players.index(p) for p in imp_list] if imp_list else [random.randint(0, len(players) - 1)]):
                p = players.pop(i)
                players_score.append(PlayerSus(player=p, sus_score=SCORE_SAFE))

            # Pick sus player
            i = random.randint(0, len(players) - 1)
            p = players.pop(i)
            players_score.append(PlayerSus(player=p, sus_score=SCORE_SUS))

            players_score += [PlayerSus(player=p, sus_score=0.5) for p in players]

            context.set_player_sus(players_score)
            print(f'Set new player list: {[f"{p.player}:{p.get_sus().name}" for p in players_score]}')
        else:
            print("Player list could not be obtained - " +
                  "make sure you're running this command in the voting panel with chat hidden.")
        print()


game_state: GameState = GameState()