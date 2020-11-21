from typing import List

from controller.helpers import prefix_match
from clients.keyboard import pop_char, get_char, handle_key
from data import enums, params
from data.state import context


def setup():
    setup_map()
    setup_me()
    while True:
        start_game()


def setup_map():
    for curr_map in [m for m in enums.AUMap if m is not enums.AUMap.COMMON]:
        print(f'{curr_map.value}: {curr_map.name}')

    print("Select map number: ", end="")
    while True:
        try:
            key = pop_char()
            if key is not None:
                context.set_state_map(enums.AUMap.__call__(int(key)))
                break
        except (ValueError, TypeError):
            pass
    set_map = context.get_state_map().name
    print(f'{set_map} selected', end='\n\n')


def setup_me():
    while True:
        print("Players: " + str(params.player))
        me = prefix_match('Which player are you? ', params.player)
        if me in params.player:
            print(f'Player {me} selected.', end='\n\n')
            break
    context.set_state_me(me)


def setup_players() -> List[str]:
    remain = params.player.copy()
    remain.remove(context.get_state_me())
    ret = []
    while True:
        print("Players in game: " + str(ret))
        print("Players not in game: " + str(remain))
        p_in = input("Type player to add (prepend - to remove) or Enter to finish: ")
        if p_in == "" and len(ret) >= 1:
            break
        remove = False
        if len(p_in) > 0 and p_in[0] == '-':
            remove = True
            p_in = p_in[1:]
        if remove:
            p = prefix_match("", ret, key=p_in)
            if p != "":
                ret.remove(p)
                remain.append(p)
                print(f'Player {p} removed.')
        else:
            p = prefix_match("", remain, key=p_in)
            if p != "":
                remain.remove(p)
                ret.append(p)
                print(f'Player {p} added.')
        print()
    return ret


def start_game():
    context.set_state_players(setup_players())
    context.set_state_game(enums.GameState.PROGRESS)
    print('\nGAME STARTED!')
    print('Press the ` key to switch to discussion mode or back to game mode.\n')
    while True:
        key = get_char()
        if key is not None:
            handle_key(key)
            if context.get_state_game() == enums.GameState.RESTART:
                print('Restarting...')
                context.set_capture_keys(False)
                context.set_state_game(enums.GameState.SETUP)
                break
