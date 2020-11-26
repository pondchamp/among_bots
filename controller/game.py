from clients import monitor, tts, keyboard
from controller import response
from controller.helpers import prefix_match
from data import enums, params
from data.state import context


def setup():
    setup_map()
    while True:
        setup_me()
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
            print(f'Player {me} selected.', end='\n\n')
            break
    context.set_me(me)


def start_game():
    context.set_game(enums.GameState.PROGRESS)
    print('\nGAME STARTED!')
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to enable bot commands.\n')
    while True:
        key = keyboard.get_char()
        if key is not None:
            state_map = context.get_map()
            state_players = context.get_players()
            mode = keyboard.handle_key(key)
            if mode == enums.KeyCommand.RESTART:
                context.set_game(enums.GameState.RESTART)
                print('Restarting...')
                context.set_capture_keys(False)
                context.set_last_response(None)
                context.set_game(enums.GameState.SETUP)
                break
            elif mode == enums.KeyCommand.REFRESH:
                players = monitor.get_players()
                me = context.get_me()
                if me in players:
                    players.remove(me)
                if players is not None and len(players) > 0:
                    context.set_players(players)
                    print(f'Set new player list: {players}')
                else:
                    print("Player list could not be obtained - " +
                          "make sure you're running this command in the voting panel with chat hidden.")
                print()
            elif mode is not None:
                resp = response.generate_response(mode, state_map, state_players)
                if resp != '':
                    tts.Speaker(resp)
                    keyboard.write_text(resp)
