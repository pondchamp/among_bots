import os


def _flag_enabled(flag: str) -> bool:
    return os.getenv(flag, None) == "1"


debug_chat = _flag_enabled('DEBUG_CHAT')
debug_net = _flag_enabled('DEBUG_NET')
debug_talk = _flag_enabled('DEBUG_TALK')
debug_pcap = _flag_enabled('DEBUG_PCAP')

GAME_TITLE = 'Among Us'
CHAT_THROTTLE_SECS = 4
SELF_SABOTAGE_PROB = 0.05
PROBE_SCORE_THRESH = 2.5
GOOGLE_APPLICATION_CREDS = "GOOGLE_APPLICATION_CREDENTIALS"
PLAYER_PREFS_FILE_LOC = os.getenv('USERPROFILE', '') + r'\AppData\LocalLow\Innersloth\Among Us\playerPrefs'
