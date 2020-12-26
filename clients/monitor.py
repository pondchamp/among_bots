import win32gui as gui


def get_foreground_window() -> str:
    return gui.GetWindowText(gui.GetForegroundWindow())
