import win32gui as gui

# Relative row positions of players
ROW_POS = [
    0.27,
    0.4,
    0.53,
    0.66,
    0.79
]

# Relative column positions of players
COL_POS = [
    0.17,
    0.515
]


def get_window_handle(name: str) -> int:
    return gui.FindWindow(None, name)


def get_colour_test(window_handle: int):
    cursor_rel_x, cursor_rel_y = get_cursor_rel_pos(window_handle)
    win_x, win_y = get_window_loc(window_handle)
    cursor_pct_x, cursor_pct_y = get_cursor_pct_pos(window_handle, cursor_rel_x, cursor_rel_y)
    if 0 <= cursor_pct_x < 1 and 0 <= cursor_pct_y < 1:
        colour = get_pixel_color(win_x + cursor_rel_x, win_y + cursor_rel_y)
        print(f'REL: {(cursor_rel_x, cursor_rel_y)}')
        print(f'POS: {(cursor_pct_x, cursor_pct_y)}')
        print(f'REL1: {get_cursor_rel_pos_from_pct(window_handle, cursor_pct_x, cursor_pct_y)}')
        print(f'COL: {colour}')


def get_player_colour(window_handle: int, player: int):
    player_x, player_y = (COL_POS[player % len(COL_POS)], ROW_POS[int(player / len(COL_POS))])
    win_x, win_y = get_window_loc(window_handle)
    player_rel_x, player_rel_y = get_cursor_rel_pos_from_pct(window_handle, player_x, player_y)
    colour = get_pixel_color(win_x + player_rel_x, win_y + player_rel_y)
    print(f'PL{player}: {(player_rel_x, player_rel_y)} -> {colour}')


def get_cursor_rel_pos(window_handle: int) -> (int, int):
    return gui.ScreenToClient(window_handle, gui.GetCursorPos())


def get_window_loc(window_handle: int) -> (int, int):
    return gui.ClientToScreen(window_handle, (0, 0))


def get_cursor_pct_pos(window_handle: int, cursor_rel_x: int, cursor_rel_y: int) -> (float, float):
    _, _, win_len, win_hgt = gui.GetClientRect(window_handle)
    return cursor_rel_x / win_len, cursor_rel_y / win_hgt


def get_cursor_rel_pos_from_pct(window_handle: int, cursor_pct_x: float, cursor_pct_y: float) -> (int, int):
    _, _, win_len, win_hgt = gui.GetClientRect(window_handle)
    return int(cursor_pct_x * win_len), int(cursor_pct_y * win_hgt)


def get_pixel_color(i_x, i_y):
    long_colour = gui.GetPixel(gui.GetDC(0), i_x, i_y)
    i_colour = int(long_colour)
    return i_colour & 0xff, (i_colour >> 8) & 0xff, (i_colour >> 16) & 0xff
