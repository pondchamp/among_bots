from typing import List, Optional


class Dialog:
    def __init__(self, text: str, max_turns: Optional[int] = None):
        self.text = text
        self.max_turns = max_turns


statement: List[Dialog] = [
    Dialog("hmm"),
    Dialog("ok"),
    Dialog("the body is in [l]", max_turns=0),
    Dialog("[l]", max_turns=0),
    Dialog("lets just skip"),
    Dialog("[p] is clear"),
    Dialog("[p] is safe"),
]

probe: List[Dialog] = [
    Dialog("where was the body", max_turns=0),
    Dialog("was anyone in [l]"),
    Dialog("where was [p]"),
    Dialog("who was in [l]"),
    Dialog("who did i just see", max_turns=1),
    Dialog("was anyone [t]"),
    Dialog("where", max_turns=0),
]

attack: List[Dialog] = [
    Dialog("where was [p]", max_turns=0),
    Dialog("[p] seems sus"),
    Dialog("[p] is sus"),
    Dialog("[p] is definitely impostor", max_turns=0),
    Dialog("I saw [p] vent", max_turns=0),
    Dialog("[p] was faking their tasks"),
    Dialog("why weren't you doing task in [l]"),
    Dialog("I'm voting [p]"),
    Dialog("[p]", max_turns=0),
    Dialog("why was [p] near the body", max_turns=0),
]

defense = [
    Dialog("I don't know"),
    Dialog("idk"),
    Dialog("no"),
    Dialog("no u"),
    Dialog("I wasn't there"),
    Dialog("I was with [p]"),
    Dialog("[p] and i were in [l]"),
    Dialog("what"),
    Dialog("i didnt vent"),
    Dialog("i was in [l]"),
    Dialog("i saw [p] last"),
    Dialog("i saw [p] in [l]"),
    Dialog("this is my first time"),
    Dialog("my tasks are done", max_turns=0),
    Dialog("i was doing my tasks"),
    Dialog("you weren't there, I was there"),
    Dialog("I was doing my tasks", max_turns=0),
    Dialog("I'm done with my tasks", max_turns=0),
    Dialog("I don't know how to do the task in [l]", max_turns=0),
    Dialog("i was doing tasks in [l]", max_turns=0),
    Dialog("i was [t]", max_turns=0),
    Dialog("thats not possible"),
    Dialog("it literally cannot be me"),
]
