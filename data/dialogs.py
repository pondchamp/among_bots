from typing import List, Optional

from data.enums import ResponseFlags as RF


class Dialog:
    def __init__(self, text: str, min_turns: Optional[int] = None, max_turns: Optional[int] = None,
                 flags: List[RF] = None):
        self.text = text
        self.max_turns = max_turns
        self.min_turns = min_turns
        self.flags = flags


statement: List[Dialog] = [
    Dialog("hmm"),
    Dialog("ok"),
    Dialog("[lb]", max_turns=0, flags=[RF.BODY_FOUND_ME]),
    Dialog("[p] is clear"),
    Dialog("[p] is safe"),
    Dialog("the body is in [lb]", max_turns=0, flags=[RF.BODY_FOUND_ME]),
    Dialog("I saw a vent but didn't see who", flags=[RF.BODY_FOUND_ME, RF.BODY_FOUND_OTHER]),
    Dialog("i saw [p] last"),
    Dialog("i saw [p] in [l]"),
]

probe: List[Dialog] = [
    Dialog("where was the body?", max_turns=0, flags=[RF.BODY_FOUND_OTHER]),
    Dialog("was anyone in [l]?"),
    Dialog("where was [p]?"),
    Dialog("who was in [l]?"),
    Dialog("who did i just see?", max_turns=1, flags=[RF.BODY_FOUND_ME]),
    Dialog("was anyone [t]?"),
    Dialog("where?", max_turns=0, flags=[RF.BODY_FOUND_OTHER]),
    Dialog("???", max_turns=0, flags=[RF.EMERGENCY_MEET_OTHER]),
    Dialog("what?", max_turns=0, flags=[RF.EMERGENCY_MEET_OTHER]),
]

attack: List[Dialog] = [
    Dialog("where was [p]?", max_turns=1),
    Dialog("[p] seems sus"),
    Dialog("[p] is sus"),
    Dialog("[p] is definitely impostor", max_turns=0),
    Dialog("I saw [p] vent", max_turns=0),
    Dialog("[p] was faking their tasks"),
    Dialog("why weren't you doing task in [l]?", min_turns=1),
    Dialog("I'm voting [p]"),
    Dialog("[p]", max_turns=0, flags=[RF.BODY_FOUND_OTHER, RF.BODY_FOUND_ME]),
    Dialog("why was [p] near the body?", flags=[RF.BODY_FOUND_OTHER, RF.BODY_FOUND_ME]),
    Dialog("i saw [p] vent in [lm]", max_turns=1, flags=[RF.EMERGENCY_MEET_ME]),
    Dialog("vote [p]"),
    Dialog("why is [p] stalking me?", max_turns=0, flags=[RF.EMERGENCY_MEET_ME]),
    Dialog("self report", flags=[RF.SELF_REPORT]),
    Dialog("I don't buy [p]'s story", min_turns=1),
]

defense = [
    Dialog("I don't know", min_turns=1),
    Dialog("idk", min_turns=1),
    Dialog("no", min_turns=1),
    Dialog("no u", min_turns=1),
    Dialog("I wasn't there"),
    Dialog("I was with [p]"),
    Dialog("[p] and i were in [lm]"),
    Dialog("what?"),
    Dialog("i didnt vent"),
    Dialog("i was in [lm]"),
    Dialog("this is my first time", min_turns=3),
    Dialog("my tasks are done"),
    Dialog("task check", max_turns=0, flags=[RF.EMERGENCY_MEET_ME]),
    Dialog("i was doing my tasks"),
    Dialog("you weren't there, I was there"),
    Dialog("I was doing my tasks", max_turns=0),
    Dialog("I'm done with my tasks", max_turns=0),
    Dialog("I don't know how to do the task in [lm]", max_turns=0),
    Dialog("i was doing tasks in [lm]", max_turns=0),
    Dialog("i was [t]", max_turns=0),
    Dialog("thats not possible"),
    Dialog("it literally cannot be me"),
    Dialog("lets just skip", min_turns=2),
]
