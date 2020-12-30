import os

debug_chat = os.getenv('DEBUG_CHAT', None) == "1"
debug_net = os.getenv('DEBUG_NET', None) == "1"

GAME_TITLE = 'Among Us'
CHAT_THROTTLE_SECS = 4
SELF_SABOTAGE_PROB = 0.1
PROBE_SCORE_THRESH = 2.5
GOOGLE_APPLICATION_CREDS = "GOOGLE_APPLICATION_CREDENTIALS"
PLAYER_PREFS_FILE_LOC = os.getenv('USERPROFILE', '') + r'\AppData\LocalLow\Innersloth\Among Us\playerPrefs'
