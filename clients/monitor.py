import win32gui as gui

from data.types import RGB, COORD


def get_foreground_window() -> str:
    return gui.GetWindowText(gui.GetForegroundWindow())


def _get_pixel_colour(i_x, i_y) -> RGB:
    long_colour = gui.GetPixel(gui.GetDC(0), i_x, i_y)
    i_colour = int(long_colour)
    return i_colour & 0xff, (i_colour >> 8) & 0xff, (i_colour >> 16) & 0xff


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
