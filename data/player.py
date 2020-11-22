from typing import Dict, List
from data.types import RGB

BG_COL: List[RGB] = [
    (187, 211, 238),
    (170, 200, 229)
]


class Player:
    def __init__(self, name: str, colour: RGB, disabled_colour: RGB):
        self.name = name
        self.colour = colour
        self.disabled_colour = disabled_colour


_player_list = [
    Player("red", (189, 64, 71), (129, 60, 65)),
    Player("blue", (61, 87, 216), (51, 70, 144)),
    Player("brown", (132, 108, 82), (89, 81, 71)),
    Player("green", (60, 148, 94), (54, 106, 79)),
    Player("pink", (219, 114, 196), (144, 86, 136)),
    Player("orange", (226, 147, 70), (142, 102, 63)),
    Player("yellow", (226, 234, 123), (85, 91, 73)),
    Player("black", (94, 106, 118), (71, 81, 91)),
    Player("white", (207, 221, 240), (48, 54, 61)),
    Player("purple", (127, 88, 200), (91, 72, 138)),
    Player("cyan", (89, 243, 225), (68, 158, 150)),
    Player("lime", (107, 232, 103), (78, 150, 83))
]


player: List[str] = [x.name for x in _player_list]
player_colour: Dict[str, RGB] = {x.name: x.colour for x in _player_list}
player_disabled_colour: Dict[str, RGB] = {x.name: x.disabled_colour for x in _player_list}
