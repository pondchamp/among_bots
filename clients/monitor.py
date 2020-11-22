import win32gui as gui
from typing import Optional, List, Tuple, Dict

from data import player, consts
from data.types import RGB, COORD

debug_cursor = True
debug_match = False

# Relative row positions of players
_ROW_POS = [
    26.11,
    38.80,
    51.49,
    64.18,
    76.87
]

# Relative column positions of players
_COL_POS = [
    15.78,
    50.00
]

_DIFF_MIN_THRESHOLD = 15


def get_foreground_window() -> str:
    return gui.GetWindowText(gui.GetForegroundWindow())


def get_window_handle(name: str) -> int:
    return gui.FindWindow(None, name)


def get_players() -> Optional[List[str]]:
    window_handle = get_window_handle(consts.GAME_TITLE)
    if debug_cursor:
        _debug_monitor(window_handle)
    diff_aggregate, players = _match_players(window_handle, player.player_colour)
    if debug_match:
        print(f'Enabled stats: {diff_aggregate}, {players}')
    diff_aggregate_disabled, players_disabled = _match_players(window_handle, player.player_disabled_colour)
    if debug_match:
        print(f'Disabled stats: {diff_aggregate_disabled}, {players_disabled}')
    voting_disabled = diff_aggregate > diff_aggregate_disabled
    print(f'{"DISCUSSION" if voting_disabled else "VOTING"} TIME')
    return players_disabled if voting_disabled else players


def _match_players(window_handle: int, arr: Dict[str, RGB]) -> Optional[Tuple[int, List[str]]]:
    players = []
    diff_aggregate = 0
    for i in range(10):
        match = _get_player_colour(window_handle, i)
        player_d, player_m = _match_player(match, arr)
        diff_aggregate += player_d
        if debug_match:
            print(f'Match: {player_m} {match} (err: {player_d})')
        if player_m is not None and player_d <= _DIFF_MIN_THRESHOLD:
            players.append(player_m)
    return diff_aggregate, players


def _get_player_colour(window_handle: int, p_i: int) -> RGB:
    player_x, player_y = (_COL_POS[p_i % len(_COL_POS)], _ROW_POS[int(p_i / len(_COL_POS))])
    win_x, win_y = _get_window_loc(window_handle)
    player_rel_x, player_rel_y = _get_cursor_rel_pos(window_handle, player_x, player_y)
    return _get_pixel_colour(win_x + player_rel_x, win_y + player_rel_y)


def _match_player(match: RGB, arr: Dict[str, RGB]) -> Tuple[int, Optional[str]]:
    diff_min: Optional[int] = None
    diff_min_player: Optional[str] = None

    # Baseline at background colour
    for b in player.BG_COL:
        diff = _calc_colour_diff(match, b)
        if diff_min is None or diff_min > diff:
            diff_min = diff

    for p in arr.items():
        diff = _calc_colour_diff(match, p[1])
        if diff_min is None or diff_min > diff:
            diff_min = diff
            diff_min_player = p[0]
    return diff_min, diff_min_player


def _calc_colour_diff(tuple1: RGB, tuple2: RGB) -> int:
    return sum(map(lambda a, b: abs(a - b), tuple1, tuple2))


def _get_pixel_colour(i_x, i_y) -> RGB:
    long_colour = gui.GetPixel(gui.GetDC(0), i_x, i_y)
    i_colour = int(long_colour)
    return i_colour & 0xff, (i_colour >> 8) & 0xff, (i_colour >> 16) & 0xff


def _get_window_loc(window_handle: int) -> COORD:
    return gui.ClientToScreen(window_handle, (0, 0))


def _get_cursor_rel_pos(window_handle: int, cursor_pct_x: float, cursor_pct_y: float) -> COORD:
    win_len, win_hgt = _get_client_rect(window_handle)
    return int(cursor_pct_x / 100 * win_len), int(cursor_pct_y / 100 * win_hgt)


def _get_client_rect(window_handle: int) -> COORD:
    _, _, win_len, win_hgt = gui.GetClientRect(window_handle)
    return win_len, win_hgt


def _debug_monitor(window_handle: int):
    cursor_pos = gui.GetCursorPos()
    cursor_x, cursor_y = gui.ScreenToClient(window_handle, cursor_pos)
    win_len, win_hgt = _get_client_rect(window_handle)
    cursor_rel = round(cursor_x / win_len * 100, 2), round(cursor_y / win_hgt * 100, 2)
    colour = _get_pixel_colour(cursor_pos[0], cursor_pos[1])
    print()
    print(f'PCT: {cursor_rel}')
    print(f'COL: {colour}')
