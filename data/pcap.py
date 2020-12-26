# Kudos: https://github.com/jordam/amongUsParser
from datetime import timedelta
import pickle

from controller.helpers import get_player_colour
from clients.pcap import PCap
from data.types import COORD
from lib.amongUsParser import parse
from lib.amongUsParser.gameEngine import GameEngine, PlayerClass
from scapy.all import *
from scapy.layers.inet import UDP

from data import enums, params, consts
from data.interpreter import Interpreter
from data.state import context

PROX_LIMIT_X = 5
PROX_LIMIT_Y = 3


class GameState:
    def __init__(self):
        self.curr_lobby: int = 0
        self._game: GameEngine = GameEngine({
            'Event': self.event_callback,
            'StartMeeting': self.start_meeting_callback,
            'StartGame': self.start_game_callback,
            'Chat': self.chat_callback,
            'RemovePlayer': self.remove_player_callback,
            'PlayerMovement': self.player_movement_callback,
        })
        PCap(self.pkt_callback)

    # CALLBACKS

    def pkt_callback(self, pkt):
        self._game.proc(pkt[UDP].payload.load, pkt.time)
        tree = parse(pkt[UDP].payload.load)
        if consts.debug_net and tree.children[0].commandName == 'ReliableData':
            tree.pprint()

    def event_callback(self, _):
        if not game_state._game.gameId:
            return
        root_dir = tempfile.gettempdir() + '\\among_bots'
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        self.cleanup_states(root_dir)
        self.update_state(root_dir)

    def start_meeting_callback(self, _):
        context.chat_log_reset()
        imp_list = self.impostor_list
        prev_player_len = len(context.get_trust_map())
        context.trust_map_players_set(self.get_players_colour(include_me=True))
        context.trust_map_score_scale(0.5)
        if prev_player_len == 0 and self.me is not None and self.me.alive:
            me = self.me_colour
            players = [x for x in self.get_players_colour() if x != me]
            context.trust_map_score_set(me, players[random.randint(0, len(players) - 1)], -0.5)
            if imp_list is not None:
                for i in imp_list:
                    context.trust_map_score_set(me, i, 1)
        self.set_player_loc()

    @staticmethod
    def start_game_callback(_):
        context.trust_map_players_reset()
        context.reset_last_seen()

    @staticmethod
    def chat_callback(state):
        interpreter = Interpreter(game_state, state['player'], state['message'].decode("utf-8"))
        interpret = interpreter.interpret()
        if interpret is not None:
            if consts.debug_chat:
                print("Trust map:")
                for x in context.get_trust_map():
                    print(x, "\t:", context.get_trust_map()[x])
                print("Aggregate:", context.trust_map_score_get())
            print()

    @staticmethod
    def remove_player_callback(event):
        if event['player'] is not None and game_state.game_started:
            player = get_player_colour(event['player'])
            context.trust_map_player_remove(player)
            players_in_frame = context.get_last_seen()
            if player in players_in_frame:
                context.remove_last_seen(player)

    def player_movement_callback(self, event):
        me = self.me
        if me is None or game_state.meeting_reason is not False:
            return
        me_id = me.playerId
        pl_id = event["player"].playerId
        player = self.get_player_from_id(pl_id)
        player_colour = get_player_colour(player)
        in_frame = self._in_frame(me_id, pl_id)
        players_in_frame = context.get_last_seen()
        if not player.alive:
            if player_colour in players_in_frame:
                context.remove_last_seen(player_colour)
            return
        if me_id == pl_id:
            players = game_state.get_players()
            if players is None:
                return
            new_pl = \
                [get_player_colour(p) for p in players
                 if p.playerId != me_id
                 and p.color is not False and p.alive
                 and self._in_frame(me_id, p.playerId)]
            for p in players_in_frame.copy():
                if p not in new_pl:
                    context.remove_last_seen(p)
            for p in new_pl.copy():
                if p in players_in_frame:
                    new_pl.remove(p)
            for p in new_pl:
                context.append_last_seen(p)
        elif in_frame and player_colour not in players_in_frame:
            context.append_last_seen(player_colour)
        elif not in_frame and player_colour in players_in_frame:
            context.remove_last_seen(player_colour)
        else:
            return

    # GETTERS AND SETTERS

    @property
    def me(self) -> Optional[PlayerClass]:
        return self._game.players.get(self._game.selfClientID)

    @property
    def me_colour(self) -> Optional[str]:
        me = self.me
        return get_player_colour(me) if me else None

    @property
    def map(self) -> Optional[enums.AUMap]:
        if self._game.gameSettings:
            au_map = self._game.gameSettings['MapId']
            return enums.AUMap.__call__(au_map)
        return None

    # DEBUG METHOD
    @map.setter
    def map(self, val: enums.AUMap):
        self._game.gameSettings['MapId'] = val

    @property
    def is_impostor(self) -> Optional[bool]:
        me = self.me
        return me.infected if me else None

    @property
    def impostor_list(self) -> Optional[List[str]]:
        if self.is_impostor and self._game.players:  # Only show if I'm impostor (no cheating!)
            return [get_player_colour(p) for p in self._game.players.values()
                    if p.infected and p.playerId != self.me.playerId]

    @property
    def meeting_started_by(self):
        return self._game.meetingStartedBy

    @property
    def meeting_reason(self):
        return self._game.meetingReason

    @property
    def game_started(self):
        return self._game.gameHasStarted

    def get_player_loc(self, player_id: int) -> COORD:
        player = self._game.playerIdMap[player_id]
        return player.x, player.y

    def set_player_loc(self):
        if self.map is None:
            return
        locations = params.location[self.map].copy()
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

    def get_players(self, include_me=False) -> Optional[List[PlayerClass]]:
        me_id = self.me.playerId if self.me is not None else -1
        if self._game.players:
            return [p for p in self._game.players.values()
                    if p.alive and (include_me or p.playerId != me_id)]
        return None

    def get_players_colour(self, include_me=False) -> Optional[List[str]]:
        return [get_player_colour(p) for p in self.get_players(include_me)]

    def get_player_from_id(self, player_id: int) -> Optional[PlayerClass]:
        if player_id not in self._game.playerIdMap:
            return None
        return self._game.playerIdMap[player_id]

    def get_player_colour_from_id(self, player_id: int) -> Optional[str]:
        if player_id not in self._game.playerIdMap:
            return None
        return get_player_colour(self._game.playerIdMap[player_id])

    # STATE MANAGEMENT

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

            # Merge state dictionaries with provided game entities
            state.entities = {**state.entities, **game_state._game.entities}
            state.players = {**state.players, **game_state._game.players}
            state.playerIdMap = {**state.playerIdMap, **game_state._game.playerIdMap}

            game_state._game = state
            with open(file_path, "wb") as fp:
                pickle.dump(state, fp)
            if consts.debug_net:
                print('Game state reloaded for game ID', game_id)
        elif game_state._game is not None:
            with open(file_path, "wb") as fp:
                pickle.dump(game_state._game, fp)
            if consts.debug_net and game_state.curr_lobby != game_id:
                print('Game state created for game ID', game_id)
        game_state.curr_lobby = game_id

    # HELPERS

    @staticmethod
    def _in_frame(me_id: int, pl_id: int) -> bool:
        me_x, me_y = game_state.get_player_loc(me_id)
        pl_x, pl_y = game_state.get_player_loc(pl_id)
        dist_x, dist_y = abs(me_x - pl_x), abs(me_y - pl_y)
        return dist_x < PROX_LIMIT_X and dist_y < PROX_LIMIT_Y


game_state: GameState = GameState()
