import random
from typing import Dict, List, Optional

from data.enums import AUMap
from data.player import player

player = player


def _jtl(tsk: str, loc_list: Optional[List[str]]):  # join task location
    if loc_list is None or len(loc_list) == 0:
        return tsk
    loc = loc_list[random.randint(0, len(loc_list))]
    if loc in ["outside"]:
        return f'{tsk} {loc}'
    return f'{tsk} in {loc}'


location: Dict[AUMap, List[str]] = {
    AUMap.COMMON: [
        "o2",
        "med bay",
        "comms",
        "storage",
        "admin",
    ],
    AUMap.SKELD: [
        "reactor",
        "cafeteria",
        "upper engine",
        "lower engine",
        "security",
        "electrical",
        "shields",
        "weapons",
    ],
    AUMap.POLUS: [
        "security",
        "electrical",
        # "left reactor",    # Emergency
        # "right reactor",   # Emergency
        "lab",
        "specimen",
        "weapons",
        "dropship",
        "south o2",
        "decontam",
        "vitals",
    ],
    AUMap.MIRA: [
        "reactor",
        "launchpad",
        "starting area",     # alias for launchpad
        "locker room",
        "decontam",
        "balcony",
        "cafeteria",
        "greenhouse",
        "hallway",
        "lab",
    ]
}

# https://among-us.fandom.com/wiki/Tasks
task: Dict[AUMap, List[str]] = {
    AUMap.SKELD: [
        _jtl("aligning engines", ["upper engine", "lower engine"]),
        _jtl("calibrating distributor", ["electrical"]),
        _jtl("charting course", ["nav"]),
        _jtl("cleaning filter", ["o2"]),
        _jtl("clearing asteroids", ["weapons"]),
        _jtl("diverting power",
             ["electrical", "comms", "lower engine", "nav", "o2", "security", "shields", "upper engine", "weapons"]),
        _jtl("emptying chute", ["o2", "storage"]),
        _jtl("emptying garbage", ["cafeteria", "storage"]),
        _jtl("fixing wiring", ["admin", "cafeteria", "electrical", "nav", "security", "storage"]),
        _jtl("fueling engines", ["storage", "lower engine", "upper engine"]),
        _jtl("inspecting samples", ["med bay"]),
        _jtl("priming shields", ["shields"]),
        _jtl("stabilising steering", ["nav"]),
        _jtl("starting reactor", None),
        _jtl("submitting scan", ["med bay"]),
        _jtl("swiping card", ["admin"]),
        _jtl("unlocking manifolds", ["reactor"]),
        _jtl("doing upload", ["cafeteria", "comms", "electrical", "nav", "weapons", "admin"])
    ],
    AUMap.POLUS: [
        _jtl("aligning telescope", ["lab"]),
        _jtl("charting course", ["dropship"]),
        _jtl("clearing asteroids", ["weapons"]),
        _jtl("emptying garbage", ["o2"]),
        _jtl("filling canisters", ["o2"]),
        _jtl("fixing weather nodes", ["outside", "lab"]),
        _jtl("fixing wiring", ["decontam", "electrical", "lab", "o2", "office"]),
        _jtl("fueling engines", ["storage", "outside"]),
        _jtl("inserting keys", ["dropship"]),
        _jtl("inspecting samples", ["lab"]),
        _jtl("monitoring tree", ["o2"]),
        _jtl("opening waterways", ["boiler room", "outside"]),
        _jtl("rebooting wifi", ["comms"]),
        _jtl("recording temperature", ["lab", "outside"]),
        _jtl("repairing drill", ["lab"]),
        _jtl("replacing water jug", ["boiler room", "office"]),
        _jtl("scanning boarding pass", ["office"]),
        _jtl("starting reactor", ["specimen"]),
        _jtl("storing artifacts", ["specimen"]),
        _jtl("submitting scan", ["lab"]),
        _jtl("swiping card", ["office"]),
        _jtl("unlocking manifolds", ["specimen"]),
        _jtl("doing upload", ["o2", "comms", "electrical", "specimen", "weapons", "office"])
    ],
    AUMap.MIRA: [
        _jtl("doing artifacts", ["lab"]),
        _jtl("buying beverage", ["cafeteria"]),
        _jtl("charting course", ["admin"]),
        _jtl("cleaning filter", ["greenhouse"]),
        _jtl("clearing asteroids", ["balcony"]),
        _jtl("diverting power",
             ["reactor", "admin", "cafeteria", "comms", "greenhouse", "lab", "launchpad", "med bay", "office"]),
        _jtl("emptying garbage", ["cafeteria"]),
        _jtl("entering id", ["admin"]),
        _jtl("fixing wiring", ["greenhouse", "hallway", "lab", "locker room", "storage"]),
        _jtl("fueling engines", ["launchpad"]),
        _jtl("measuring weather", ["balcony"]),
        _jtl("priming shields", ["admin"]),
        _jtl("processing data", ["office"]),
        _jtl("running diagnostics", ["launchpad"]),
        _jtl("sorting samples", ["lab"]),
        _jtl("starting reactor", None),
        _jtl("submitting scan", ["med bay"]),
        _jtl("unlocking manifolds", ["reactor"]),
        _jtl("watering plants", ["storage", "greenhouse"])
    ]
}