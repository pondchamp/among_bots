import os

debug_chat = os.getenv('DEBUG_CHAT', None) == "1"
debug_net = os.getenv('DEBUG_NET', None) == "1"
GAME_TITLE = 'Among Us'
CHAT_THROTTLE_SECS = 4
