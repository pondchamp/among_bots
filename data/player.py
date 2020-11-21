from typing import Dict, List

RGB = (int, int, int)


class Player:
    def __init__(self, name: str, colour: RGB, dead_colour: RGB):
        self.name = name
        self.colour = colour
        self.dead_colour = dead_colour


_player_list = [
    Player("red", (189, 64, 71), None),
    Player("blue", (61, 87, 216), None),
    Player("brown", (132, 108, 82), None),
    Player("green", (60, 148, 94), None),
    Player("pink", (222, 115, 198), None),
    Player("orange", (226, 147, 70), None),
    Player("yellow", (226, 234, 123), None),
    Player("black", (94, 106, 118), None),
    Player("white", (207, 221, 240), None),
    Player("purple", (127, 88, 200), None),
    Player("cyan", (89, 243, 225), None),
    Player("lime", (107, 232, 103), None)
]


player: List[str] = [x.name for x in _player_list]
player_info: Dict[str, Player] = {x.name: x for x in _player_list}
