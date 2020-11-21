RGB = (int, int, int)


class Player:
    def __init__(self, name: str, colour: RGB, dead_colour: RGB):
        self.name = name
        self.colour = colour
        self.dead_colour = dead_colour


_player_list = [
    Player("red", None, None),
    Player("blue", None, None),
    Player("brown", None, None),
    Player("green", None, None),
    Player("pink", None, None),
    Player("orange", None, None),
    Player("yellow", None, None),
    Player("black", None, None),
    Player("white", None, None),
    Player("purple", None, None),
    Player("cyan", None, None),
    Player("lime", None, None),
    Player("dark green", None, None)
]


player = [x.name for x in _player_list]
