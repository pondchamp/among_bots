# Kudos: https://github.com/jordam/amongUsParser
from datetime import datetime, timedelta
import os
import pickle
import random
from typing import List, Optional, Dict, Callable

from lib.amongUsParser import parse
from lib.amongUsParser.gameEngine import GameEngine, PlayerClass
from scapy.layers.inet import UDP

from controller.helpers import get_player_colour
from clients.pcap import PCap
from data import enums, params, consts
from data.enums import ResponseFlags as RF
from data.state import context
from data.trust import SusScore
from data.types import COORD


class GameState:
    def __init__(self):
        self.curr_lobby: int = 0
        self._game: GameEngine = GameEngine()
        PCap(self.pkt_callback)

    # CALLBACKS

    @property
    def cb(self):
        return self._game.callbackDict

    @cb.setter
    def cb(self, cb: Dict[str, Callable]):
        self._game.callbackDict = cb

    def pkt_callback(self, pkt):
        self._game.proc(pkt[UDP].payload.load, pkt.time)
        tree = parse(pkt[UDP].payload.load)
        if consts.debug_net and tree.children[0].commandName == 'ReliableData':
            tree.pprint()

    # GETTERS AND SETTERS

    @property
    def game_id(self) -> Optional[int]:
        return self._game.gameId if self._game.gameId else None

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
        context.player_loc = loc_dict
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

    def update_state(self, root_dir: str):
        game_id = self._game.gameId
        file_path = root_dir + '\\' + str(game_id)
        if self.curr_lobby != game_id and os.path.exists(file_path):
            with open(file_path, "rb") as fp:
                try:
                    state: GameEngine = pickle.load(fp)
                except EOFError:
                    return
            state.callbackDict = self._game.callbackDict
            # Update self client ID details
            if self._game.selfClientID:
                state.players[self._game.selfClientID] = state.players[state.selfClientID]
                del state.players[state.selfClientID]
                state.selfClientID = self._game.selfClientID
            for i in state.players.keys():
                state.players[i].self = self._game

            # Merge state dictionaries with provided game entities
            state.entities = {**state.entities, **self._game.entities}
            state.players = {**state.players, **self._game.players}
            state.playerIdMap = {**state.playerIdMap, **self._game.playerIdMap}

            self._game = state
            with open(file_path, "wb") as fp:
                pickle.dump(state, fp)
            if consts.debug_net:
                print('Game state reloaded for game ID', game_id)
        elif self._game is not None:
            with open(file_path, "wb") as fp:
                pickle.dump(self._game, fp)
            if consts.debug_net and self.curr_lobby != game_id:
                print('Game state created for game ID', game_id)
        self.curr_lobby = game_id

    # HELPERS

    def get_response_flags(self) -> List[RF]:
        flags = []
        me = self.me
        reason = self.meeting_reason
        start_by = self.meeting_started_by
        if random.random() < consts.SELF_SABOTAGE_PROB:
            flags.append(RF.SELF_SABOTAGE)
        if me is not None and me.infected:
            flags.append(RF.SELF_IMPOSTOR)
        if reason is not False and start_by is not False:
            start_by_me = me is not None and start_by.playerId == me.playerId
            if reason == 'Button':
                flag = RF.EMERGENCY_MEET_ME if start_by_me else RF.EMERGENCY_MEET_OTHER
            else:  # Body found
                flag = RF.BODY_FOUND_ME if start_by_me else RF.BODY_FOUND_OTHER
                if flag == RF.BODY_FOUND_OTHER:
                    player_colour = self.get_player_colour_from_id(start_by.playerId)
                    trust_scores = context.trust_map_score_get()
                    if player_colour in [p for p in trust_scores if trust_scores[p] == SusScore.SUS.value]:
                        flags.append(RF.SELF_REPORT)
            flags.append(flag)

        return flags
