from clients import monitor, tts, keyboard
from clients.pcap import game_state
from controller import response
from data import enums, consts
from data.state import context


def start_game():
    print('\nGAME STARTED!')
    swap_key = enums.KeyCommand.KEY_CAP.value
    print(f'Press the {swap_key} key while in-game to enable bot commands.\n')
    while True:
        if not _in_game():
            continue
        key = keyboard.get_char()
        if key is not None:
            mode = keyboard.handle_key(key)
            if mode == enums.KeyCommand.HELP:
                keyboard.print_commands()
                print()
            elif mode is not None:
                resp = response.generate_response(mode, context.get_player_sus(), game_state.get_map())
                if resp != '':
                    tts.Speaker(resp)
                    keyboard.write_text(resp)
                    chat_turns = context.get_chat_turns()
                    print(f"Response #{chat_turns}: {resp}")
                    context.set_chat_turns(chat_turns + 1)


def _in_game() -> bool:
    window_name = monitor.get_foreground_window()
    return window_name == consts.GAME_TITLE
