from controller.helpers import prefix_match
from clients.keyboard import get_char, handle_key
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
            key = get_char()
            if key is not None:
                context.set_map(enums.AUMap.__call__(int(key)))
                break
        except (ValueError, TypeError):
            pass
    set_map = context.get_map().name
    print(f'{set_map} selected', end='\n\n')


def setup_me():
    while True:
        print("Players: " + str(params.player))
        me = prefix_match('Which player are you? ', params.player)
        if me in params.player:
            print(f'Player {me} selected.', end='\n\n')
            break
    context.set_me(me)


def start_game():
    context.set_game(enums.GameState.PROGRESS)
    print('\nGAME STARTED!')
    print('Press the ` key while in-game to switch to discussion mode or back to game mode.\n')
    while True:
        key = get_char()
        if key is not None:
            handle_key(key)
            if context.get_game() == enums.GameState.RESTART:
                print('Restarting...')
                context.set_capture_keys(False)
                context.set_game(enums.GameState.SETUP)
                break
