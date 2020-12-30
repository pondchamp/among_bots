from typing import List, Optional

from data.enums import ResponseFlags as rF


class Dialog:
    def __init__(self, text: str, min_turns: Optional[int] = None, max_turns: Optional[int] = None,
                 flags: List[rF] = None):
        self.text = text
        self.max_turns = max_turns
        self.min_turns = min_turns
        self.flags = flags


statement: List[Dialog] = [
    Dialog("hmm"),
    Dialog("ok"),
    Dialog("[p] is clear"),
    Dialog("[p] is safe"),
    Dialog("i saw [pn] last"),
    Dialog("i saw [p] in [l]"),
    Dialog("orang", max_turns=0, flags=[rF.SELF_SABOTAGE]),

    Dialog("[lb]", max_turns=0, flags=[rF.BODY_FOUND_ME]),
    Dialog("the body is in [lb]", max_turns=0, flags=[rF.BODY_FOUND_ME]),
    Dialog("I saw a vent but didn't see who", flags=[rF.BODY_FOUND_ME]),

    Dialog("task check", max_turns=0, flags=[rF.EMERGENCY_MEET_ME]),

    Dialog("what", max_turns=0, flags=[rF.EMERGENCY_MEET_OTHER]),
]

probe: List[Dialog] = [
    Dialog("was anyone in [l]?"),
    Dialog("where was [p]?"),
    Dialog("who was in [l]?"),
    Dialog("was anyone [t]?"),
    Dialog("orang", max_turns=0, flags=[rF.SELF_SABOTAGE]),

    Dialog("who did i just see?", max_turns=1, flags=[rF.BODY_FOUND_ME]),

    Dialog("where was the body?", max_turns=0, flags=[rF.BODY_FOUND_OTHER]),
    Dialog("where?", max_turns=0, flags=[rF.BODY_FOUND_OTHER]),

    Dialog("who just vented in front of me?", max_turns=0, flags=[rF.EMERGENCY_MEET_ME]),

    Dialog("???", max_turns=0, flags=[rF.EMERGENCY_MEET_OTHER]),
    Dialog("what?", max_turns=0, flags=[rF.EMERGENCY_MEET_OTHER]),
]

attack: List[Dialog] = [
    Dialog("[pn]", max_turns=0, flags=[rF.PRIORITY]),

    Dialog("where was [p]?", max_turns=1),
    Dialog("[p] seems sus"),
    Dialog("[p] is sus"),
    Dialog("[p] is definitely impostor", max_turns=0),
    Dialog("I saw [pn] vent", max_turns=0),
    Dialog("[pn] was faking their tasks"),
    Dialog("why weren't you doing task in [l]?", min_turns=1),
    Dialog("I'm voting [p]"),
    Dialog("vote [p]"),
    Dialog("I don't buy [p]'s story", min_turns=1),
    Dialog("orang", max_turns=0, flags=[rF.SELF_SABOTAGE]),

    Dialog("why was [pn] near the body?", flags=[rF.BODY_FOUND_OTHER, rF.BODY_FOUND_ME]),
    Dialog("self report", flags=[rF.SELF_REPORT]),  # implies BODY_FOUND_OTHER

    Dialog("i saw [pn] vent in [lm]", max_turns=1, flags=[rF.EMERGENCY_MEET_ME]),
    Dialog("why is [pn] stalking me?", max_turns=0, flags=[rF.EMERGENCY_MEET_ME]),
]

defense = [
    Dialog("I don't know", min_turns=1),
    Dialog("idk", min_turns=1),
    Dialog("no", min_turns=1),
    Dialog("no u", min_turns=1),
    Dialog("I wasn't there"),
    Dialog("I was with [pn]"),
    Dialog("[pn] and i were in [lm]"),
    Dialog("what?"),
    Dialog("i was in [lm]"),
    Dialog("i didnt vent", flags=[rF.SELF_SABOTAGE]),
    Dialog("this is my first time", min_turns=2, flags=[rF.SELF_SABOTAGE]),
    Dialog("my tasks are done"),
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
