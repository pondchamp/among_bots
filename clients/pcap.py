# Kudos: https://github.com/jordam/amongUsParser
from datetime import timedelta
import pickle

from lib.amongUsParser import parse
from lib.amongUsParser.gameEngine import GameEngine, PlayerClass
from scapy.all import *
from scapy.layers.inet import UDP

from data import enums, params
from data.interpreter import Interpreter
from data.state import context
from data.sus_score import PlayerSus, SCORE_SUS, SCORE_SAFE, SusScore

debug = False


def _get_player_colour(p: PlayerClass) -> str:
    return enums.PlayerColour.__call__(p.color).name.lower()


class GameState(Thread):
    def __init__(self):
        self.curr_lobby: int = 0
        self._game: GameEngine = GameEngine({
            'Event': self.event_callback,
            'StartMeeting': self.start_meeting_callback,
            'Chat': self.chat_callback,
        })
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        sniff(prn=self.pkt_callback,
              filter="udp portrange 22023-22923",
              store=0)

    def pkt_callback(self, pkt):
        self._game.proc(pkt[UDP].payload.load, pkt.time)
        tree = parse(pkt[UDP].payload.load)
        if debug and tree.children[0].commandName == 'ReliableData':
            tree.pprint()

    def get_me(self) -> Optional[PlayerClass]:
        return self._game.players[self._game.selfClientID] if self._game.selfClientID in self._game.players else None

    def get_me_colour(self) -> Optional[str]:
        me = self.get_me()
        return _get_player_colour(me) if me else None

    def get_map(self) -> Optional[enums.AUMap]:
        if self._game.gameSettings:
            au_map = self._game.gameSettings['MapId']
            return enums.AUMap.__call__(au_map)
        return None

    # DEBUG METHOD
    def set_map(self, val: enums.AUMap):
        self._game.gameSettings['MapId'] = val

    def get_impostor_count(self) -> Optional[int]:
        if self._game.gameSettings:
            return self._game.gameSettings['NumImpostors']
        return None

    def get_players(self) -> Optional[List[str]]:
        me_id = self.get_me().playerId if self.get_me() is not None else -1
        if self._game.players:
            return [_get_player_colour(p) for p in self._game.players.values()
                    if p.alive and p.playerId != me_id]
        return None

    def get_player_from_id(self, player_id: int) -> Optional[str]:
        if player_id not in self._game.playerIdMap:
            return None
        return _get_player_colour(self._game.playerIdMap[player_id])

    def get_is_impostor(self) -> Optional[bool]:
        me = self.get_me()
        return me.infected if me else None

    def get_impostor_list(self) -> Optional[List[str]]:
        if self.get_is_impostor() and self._game.players:  # Only show if I'm impostor (no cheating!)
            return [_get_player_colour(p) for p in self._game.players.values()
                    if p.infected and p.playerId != self.get_me().playerId]

    def get_meeting_started_by(self):
        return self._game.meetingStartedBy

    def get_meeting_reason(self):
        return self._game.meetingReason

    def start_meeting_callback(self, _):
        context.chat_log_reset()
        self.set_player_sus(self.get_players(), self.get_impostor_list())
        self.set_player_loc()

    @staticmethod
    def chat_callback(state):
        interpreter = Interpreter(game_state, state['player'], state['message'].decode("utf-8"))
        print(interpreter.interpret())

    def event_callback(self, _):
        if not game_state._game.gameId:
            return
        root_dir = tempfile.gettempdir() + '\\among_bots'
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        self.cleanup_states(root_dir)
        self.update_state(root_dir)

    @staticmethod
    def cleanup_states(root_dir: str):
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            last_mod = datetime.fromtimestamp(os.stat(file_path).st_mtime)
            time_since_mod = datetime.now() - last_mod
            expiry = timedelta(hours=1)
            if time_since_mod > expiry:
                os.remove(file_path)

    @staticmethod
    def update_state(root_dir: str):
        game_id = game_state._game.gameId
        file_path = root_dir + '\\' + str(game_id)
        if game_state.curr_lobby != game_id and os.path.exists(file_path):
            with open(file_path, "rb") as fp:
                try:
                    state: GameEngine = pickle.load(fp)
                except EOFError:
                    return
            state.callbackDict = game_state._game.callbackDict
            # Update self client ID details
            if game_state._game.selfClientID:
                state.players[game_state._game.selfClientID] = state.players[state.selfClientID]
                del state.players[state.selfClientID]
                state.selfClientID = game_state._game.selfClientID
                for i in state.players.keys():
                    state.players[i].game_state = game_state._game
                game_state._game = state
            with open(file_path, "wb") as fp:
                pickle.dump(state, fp)
            print('Game state reloaded for game ID', game_id)
        elif game_state._game is not None:
            with open(file_path, "wb") as fp:
                pickle.dump(game_state._game, fp)
            if game_state.curr_lobby != game_id:
                print('Game state created for game ID', game_id)
        game_state.curr_lobby = game_id

    @staticmethod
    def set_player_sus(players, imp_list=None):
        if players is not None and len(players) > 0:
            players_score: List[PlayerSus] = []

            # Pick safe player/s
            default_index = random.randint(0, len(players) - 1)
            for p in (imp_list if imp_list is not None else [players[default_index]]):
                players.remove(p)
                players_score.append(PlayerSus(player=p, sus_score=SCORE_SAFE))

            # Pick sus player
            i = random.randint(0, len(players) - 1)
            p = players.pop(i)
            players_score.append(PlayerSus(player=p, sus_score=SCORE_SUS))

            players_score += [PlayerSus(player=p, sus_score=0.5) for p in players]

            context.set_player_sus(players_score)
            print('Set new player list:',
                  [f"{p.player}:{p.get_sus().name}" for p in players_score if p.get_sus() != SusScore.IDK])
        else:
            print("Player list could not be obtained.")

    def set_player_loc(self):
        if self.get_map() is None:
            return
        locations = params.location[self.get_map()].copy()
        me_loc = locations[random.randint(0, len(locations) - 1)]
        locations.remove(me_loc)
        body_loc = locations[random.randint(0, len(locations) - 1)]
        locations.remove(body_loc)
        loc_dict = {
            'me': me_loc,
            'body': body_loc,
        }
        context.set_player_loc(loc_dict)
        print('Set new location list:',
              [f'{k}: {v}' for k, v in loc_dict.items()])


game_state: GameState = GameState()
