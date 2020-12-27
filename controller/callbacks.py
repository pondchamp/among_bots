import os
import random
import tempfile

from controller.helpers import get_player_colour
from data import consts
from data.interpreter import Interpreter
from state import helpers
from state.context import context

PROX_LIMIT_X = 5
PROX_LIMIT_Y = 3


class Callbacks:
    def __init__(self, game_state):  # Untyped due to circular reference
        """
        Initialises the callback dictionary set for the Among Us parser.
        :param game_state: A GameState object.
        """
        self._game = game_state

    @property
    def cb(self):
        return {
            'Event': self.event_callback,
            'StartMeeting': self.start_meeting_callback,
            'StartGame': self.start_game_callback,
            'Chat': self.chat_callback,
            'RemovePlayer': self.remove_player_callback,
            'PlayerMovement': self.player_movement_callback,
        }

    @property
    def root_dir(self):
        return tempfile.gettempdir() + '\\among_bots'
        
    def event_callback(self, _):
        if not self._game.game_id:
            return
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        helpers.cleanup_states(self.root_dir)
        if self._game.game_id is not None:
            context.update_state(self._game, self.root_dir)
        self._game.update_state(self.root_dir)
    
    def start_meeting_callback(self, _):
        context.chat_log_reset()
        imp_list = self._game.impostor_list
        prev_player_len = len(context.trust_map)
        context.trust_map_players_set(self._game.get_players_colour(include_me=True))
        context.trust_map_score_scale(0.5)
        if prev_player_len == 0 and self._game.me is not None and self._game.me.alive:
            me = self._game.me_colour
            players = [x for x in self._game.get_players_colour() if x != me]
            context.trust_map_score_set(me, players[random.randint(0, len(players) - 1)], -0.5)
            if imp_list is not None:
                for i in imp_list:
                    context.trust_map_score_set(me, i, 1)
        self._game.set_player_loc()

    @staticmethod
    def start_game_callback(_):
        context.trust_map_players_reset()
        context.last_seen_reset()
    
    def chat_callback(self, event):
        interpreter = Interpreter(self._game, event['player'], event['message'].decode("utf-8"))
        interpret = interpreter.interpret()
        if interpret is not None:
            if consts.debug_chat:
                print("Trust map:")
                for x in context.trust_map:
                    print(x, "\t:", context.trust_map[x])
                print("Aggregate:", context.trust_map_score_get())
            print()
    
    def remove_player_callback(self, event):
        if event['player'] is not None and self._game.game_started:
            player = get_player_colour(event['player'])
            context.trust_map_player_remove(player)
            players_in_frame = context.last_seen
            if player in players_in_frame:
                context.last_seen_remove(player)

    def player_movement_callback(self, event):
        me = self._game.me
        if me is None or self._game.meeting_reason is not False:
            return
        me_id = me.playerId
        pl_id = event["player"].playerId
        player = self._game.get_player_from_id(pl_id)
        player_colour = get_player_colour(player)
        in_frame = self._in_frame(me_id, pl_id)
        players_in_frame = context.last_seen
        if not player.alive:
            if player_colour in players_in_frame:
                context.last_seen_remove(player_colour)
            return
        if me_id == pl_id:
            players = self._game.get_players()
            if players is None:
                return
            new_pl = \
                [get_player_colour(p) for p in players
                 if p.playerId != me_id
                 and p.color is not False and p.alive
                 and self._in_frame(me_id, p.playerId)]
            for p in players_in_frame.copy():
                if p not in new_pl:
                    context.last_seen_remove(p)
            for p in new_pl.copy():
                if p in players_in_frame:
                    new_pl.remove(p)
            for p in new_pl:
                context.last_seen_append(p)
        elif in_frame and player_colour not in players_in_frame:
            context.last_seen_append(player_colour)
        elif not in_frame and player_colour in players_in_frame:
            context.last_seen_remove(player_colour)
        else:
            return
    
    def _in_frame(self, me_id: int, pl_id: int) -> bool:
        me_x, me_y = self._game.get_player_loc(me_id)
        pl_x, pl_y = self._game.get_player_loc(pl_id)
        dist_x, dist_y = abs(me_x - pl_x), abs(me_y - pl_y)
        return dist_x < PROX_LIMIT_X and dist_y < PROX_LIMIT_Y
