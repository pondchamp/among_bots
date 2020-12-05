import random
from typing import List, Optional

from clients import monitor, tts, keyboard
from clients.pcap import GameState
from controller import response
from controller.helpers import num_to_key, key_to_num
from data import enums, params, consts
from data.state import context
from data.sus_score import PlayerSus, SCORE_SUS, SCORE_SAFE

game_state = GameState()


def setup():
    while True:
        start_game()


def start_game():
    print('\nGAME STARTED!')
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to enable bot commands.\n')
    while True:
        if not _in_game():
            continue
        key = keyboard.get_char()
        if key is not None:
            state_map = game_state.get_map()
            state_players = _get_player_sus()
            mode = keyboard.handle_key(key)
            if mode == enums.KeyCommand.IMPOSTOR_MODE:
                _toggle_impostors()
            elif mode == enums.KeyCommand.REFRESH:
                context.set_chat_turns(0)
            elif mode == enums.KeyCommand.HELP:
                print_commands()
                print()
            elif mode is not None:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    tts.Speaker(resp)
                    keyboard.write_text(resp)
                    chat_turns = context.get_chat_turns()
                    print(f"Response #{chat_turns}: {resp}")
                    context.set_chat_turns(chat_turns + 1)


def _toggle_impostors():
    (is_imp, _) = context.get_is_impostor()
    is_imp = not is_imp
    imp_col = []
    if is_imp:
        me = game_state.get_me()
        num_imp = game_state.get_impostor_count()
        num_imp -= 1
        for _ in range(num_imp):
            imp = _select_player([p for p in params.player if p != me and p not in imp_col])
            imp_col.append(imp)
    context.set_is_impostor((is_imp, imp_col if is_imp else None))
    print(f"IMPOSTOR MODE {'ENABLED' if is_imp else 'DISABLED'}")


def _get_player_sus() -> Optional[List[PlayerSus]]:
    players = game_state.get_players()
    me = game_state.get_me()
    if me in players:
        players.remove(me)
    if players is not None and len(players) > 0:
        players_score: List[PlayerSus] = []

        # Pick sus player/s
        for _ in range(game_state.get_impostor_count()):
            i = random.randint(0, len(players) - 1)
            p = players.pop(i)
            players_score.append(PlayerSus(player=p, sus_score=SCORE_SUS))

        # Pick safe player
        if len(players) > 0:
            i = random.randint(0, len(players) - 1)
            p = players.pop(i)
            players_score.append(PlayerSus(player=p, sus_score=SCORE_SAFE))

        players_score += [PlayerSus(player=p, sus_score=0.5) for p in players]

        print(f'Set new player list: {[f"{p.player}:{p.get_sus().name}" for p in players_score]}')
        return players_score
    else:
        print("Player list could not be obtained - " +
              "make sure you're running this command in the voting panel with chat hidden.")
    print()
    return None


def _select_player(player_list: List[str], player_type: str = "player") -> str:
    print("Players:")
    for i in range(len(player_list)):
        print(f'{num_to_key(i + 1)}: {player_list[i]}')
    print(f"Select colour of {player_type}: ", end="")
    while True:
        key = keyboard.get_char()
        if key is not None:
            colour = key_to_num(key)
            if colour is not None:
                keyboard.backspace()
                player = player_list[colour - 1]
                print(f'Player {player} selected.', end='\n\n')
                return player


def print_commands():
    print(game_state.get_me())
    if game_state.get_map():
        print(game_state.get_map().name)
    print(game_state.get_impostor_count())
    print("COMMANDS")
    for x in [x for x in enums.KeyCommand if x != enums.KeyCommand.KEY_CAP]:
        k = x.value
        v = str.title(x.name).replace('_', ' ')
        current = None
        if x == enums.KeyCommand.IMPOSTOR_MODE:
            current = context.get_is_impostor()[0]
        print(f'{k}: {v}{f" (Current: {str(current).title()})" if current is not None else ""}')


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE
