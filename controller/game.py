import random
from typing import List

from clients import monitor, tts, keyboard
from controller import response
from controller.helpers import prefix_match
from data import enums, params, consts
from data.state import context
from data.sus_score import PlayerSus, SCORE_SUS, SCORE_SAFE


def setup():
    setup_map()
    while True:
        setup_me()
        setup_impostor()
        start_game()


def setup_map():
    for curr_map in [m for m in enums.AUMap if m is not enums.AUMap.COMMON]:
        print(f'{curr_map.value}: {curr_map.name}')

    print("Select map number: ", end="")
    while True:
        try:
            key = keyboard.get_char()
            if key is not None:
                context.set_map(enums.AUMap.__call__(int(key)))
                break
        except (ValueError, TypeError):
            pass
    keyboard.backspace()
    set_map = context.get_map().name
    print(f'{set_map} selected', end='\n\n')


def setup_me():
    while True:
        print("Players: " + str(params.player))
        me = prefix_match('Which player are you? ', params.player)
        if me in params.player:
            break
    print(f'Player {me} selected.', end='\n\n')
    context.set_me(me)


def setup_impostor():
    print("Number of impostors: ", end="")
    while True:
        try:
            key = keyboard.get_char()
            if key is not None:
                context.set_num_impostor(int(key))
                break
        except (ValueError, TypeError):
            pass
    keyboard.backspace()
    set_imp = context.get_num_impostor()
    print(f'{set_imp} impostor', end='\n\n')


def start_game():
    context.set_game(enums.GameState.PROGRESS)
    print('\nGAME STARTED!')
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to enable bot commands.\n')
    while True:
        if not _in_game():
            continue
        key = keyboard.get_char()
        if key is not None:
            state_map = context.get_map()
            state_players = context.get_players()
            mode = keyboard.handle_key(key)
            if mode == enums.KeyCommand.RESTART:
                _restart_game()
                break
            elif mode == enums.KeyCommand.REFRESH:
                _refresh_players()
            elif mode is not None:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    tts.Speaker(resp)
                    keyboard.write_text(resp)


def _restart_game():
    context.set_game(enums.GameState.RESTART)
    print('Restarting...')
    context.set_capture_keys(False)
    context.set_last_response(None)
    context.set_game(enums.GameState.SETUP)


def _refresh_players():
    players = monitor.get_players()
    me = context.get_me()
    if me in players:
        players.remove(me)
    if players is not None and len(players) > 0:
        players_score: List[PlayerSus] = []

        # Pick sus player/s
        for _ in range(context.get_num_impostor()):
            i = random.randint(0, len(players) - 1)
            p = players.pop(i)
            players_score.append(PlayerSus(player=p, sus_score=SCORE_SUS))

        # Pick safe player
        i = random.randint(0, len(players) - 1)
        p = players.pop(i)
        players_score.append(PlayerSus(player=p, sus_score=SCORE_SAFE))

        players_score += [PlayerSus(player=p, sus_score=0.5) for p in players]

        context.set_players(players_score)
        print(f'Set new player list: {[f"{p.player}:{p.get_sus().name}" for p in players_score]}')
    else:
        print("Player list could not be obtained - " +
              "make sure you're running this command in the voting panel with chat hidden.")
    print()


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE
