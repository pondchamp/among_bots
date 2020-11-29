import random
from typing import List

from clients import monitor, tts, keyboard
from controller import response
from controller.helpers import num_to_key, key_to_num
from data import enums, params, consts
from data.state import context
from data.sus_score import PlayerSus, SCORE_SUS, SCORE_SAFE


def setup():
    setup_map()
    setup_impostor()
    while True:
        setup_me()
        start_game()


def setup_map():
    for curr_map in [m for m in enums.AUMap if m is not enums.AUMap.COMMON]:
        print(f'{curr_map.value + 1}: {curr_map.name}')

    print("Select map number: ", end="")
    while True:
        try:
            key = keyboard.get_char()
            if key is not None:
                key_int = int(key)
                if key_int <= 0:
                    continue
                context.set_map(enums.AUMap.__call__(key_int - 1))
                break
        except (ValueError, TypeError):
            pass
    keyboard.backspace()
    set_map = context.get_map().name
    print(f'{set_map} selected', end='\n\n')


def setup_me():
    print("Players:")
    for i in range(len(params.player)):
        print(f'{num_to_key(i + 1)}: {params.player[i]}')
    print("Select your player colour: ", end="")
    while True:
        key = keyboard.get_char()
        if key is not None:
            colour = key_to_num(key)
            if colour is not None:
                me = params.player[colour - 1]
                break
    print(f'Player {me} selected.', end='\n\n')
    context.set_me(me)


def setup_impostor():
    print("Number of impostors: ", end="")
    while True:
        try:
            key = keyboard.get_char()
            if key is not None:
                key_int = int(key)
                if 1 <= key_int <= 3:
                    context.set_num_impostor(key_int)
                    break
        except (ValueError, TypeError):
            pass
    keyboard.backspace()
    set_imp = context.get_num_impostor()
    print(f'{set_imp} impostor{"s" if set_imp > 1 else ""}', end='\n\n')


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
            if mode == enums.KeyCommand.CHANGE_IMPOSTOR_COUNT:
                setup_impostor()
            elif mode == enums.KeyCommand.CHANGE_MAP:
                setup_map()
            elif mode == enums.KeyCommand.CHANGE_PLAYER:
                setup_me()
            elif mode == enums.KeyCommand.REFRESH:
                _refresh_players()
            elif mode == enums.KeyCommand.HELP:
                print_commands()
                print()
            elif mode is not None:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    tts.Speaker(resp)
                    keyboard.write_text(resp)


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
        if len(players) > 0:
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


def print_commands():
    for x in [x for x in enums.KeyCommand if x != enums.KeyCommand.KEY_CAP]:
        k = x.value
        v = str.lower(x.name).replace('_', ' ')
        current = None
        if x == enums.KeyCommand.CHANGE_PLAYER:
            current = context.get_me()
        elif x == enums.KeyCommand.CHANGE_IMPOSTOR_COUNT:
            current = context.get_num_impostor()
        elif x == enums.KeyCommand.CHANGE_MAP:
            current = context.get_map().name
        print(f'{k}: {v}{f" (Current: {current})" if current is not None else ""}')


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE
