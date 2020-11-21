import data.player as player
from data.enums import AUMap

player = player.player

location = {
    -1: [
        "o2",
        "med bay",
        "comms",
        "storage",
        "admin",
        "hallway"
    ],
    AUMap.SKELD: [
        "reactor",
        "cafeteria",
        "upper engine",
        "lower engine",
        "security",
        "electrical",
        "shields",
        "weapons"
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
        "vitals"
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
        "lab"
    ]
}

# https://among-us.fandom.com/wiki/Tasks
task = {
    -1: [
        "charting course",
        "clearing asteroids",
        "emptying garbage",
        "starting reactor",
        "unlocking manifolds"
    ],
    AUMap.SKELD: [
        "aligning engines",
        "calibrating distributor",
        "cleaning filter",
        "diverting power",
        "emptying chute",
        "fixing wiring",
        "fueling engines",
        "inspecting samples",
        "priming shields",
        "stabilising steering",
        "submitting scan",
        "swiping card",
        "doing upload"
    ],
    AUMap.POLUS: [
        "aligning telescope",
        "filling canisters",
        "fixing weather node",
        "inserting keys",
        "inspecting samples",
        "monitoring tree",
        "opening waterways",
        "rebooting wifi",
        "recording temperature",
        "repairing drill",
        "replacing water jug",
        "scanning boarding pass",
        "storing artifacts",
        "swiping card",
        "doing upload"
    ],
    AUMap.MIRA: [
        "doing artifacts",
        "using vending machine",
        "cleaning filter",
        "diverting power",
        "entering id",
        "measuring weather",
        "priming shields",
        "processing data",
        "running diagnostics",
        "sorting samples",
        "watering plants"
    ]
}
