import win32gui as gui
from typing import Optional, List

from data import player

# Relative row positions of players
_ROW_POS = [
    0.27,
    0.4,
    0.53,
    0.66,
    0.79
]

# Relative column positions of players
_COL_POS = [
    0.17,
    0.515
]


def get_window_handle(name: str) -> int:
    return gui.FindWindow(None, name)


def get_players(window_handle: int) -> Optional[List[str]]:
    players = []
    for i in range(10):
        match = get_player_colour(window_handle, i)
        for p in player.player_info.values():
            if p.colour == match:
                players.append(p.name)
                break
    return players


def get_player_colour(window_handle: int, p_i: int):
    player_x, player_y = (_COL_POS[p_i % len(_COL_POS)], _ROW_POS[int(p_i / len(_COL_POS))])
    win_x, win_y = _get_window_loc(window_handle)
    player_rel_x, player_rel_y = _get_cursor_rel_pos(window_handle, player_x, player_y)
    return _get_pixel_color(win_x + player_rel_x, win_y + player_rel_y)


def _get_window_loc(window_handle: int) -> (int, int):
    return gui.ClientToScreen(window_handle, (0, 0))


def _get_cursor_rel_pos(window_handle: int, cursor_pct_x: float, cursor_pct_y: float) -> (int, int):
    _, _, win_len, win_hgt = gui.GetClientRect(window_handle)
    return int(cursor_pct_x * win_len), int(cursor_pct_y * win_hgt)


def _get_pixel_color(i_x, i_y):
    long_colour = gui.GetPixel(gui.GetDC(0), i_x, i_y)
    i_colour = int(long_colour)
    return i_colour & 0xff, (i_colour >> 8) & 0xff, (i_colour >> 16) & 0xff
