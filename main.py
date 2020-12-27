import os

from clients.keyboard import new_listener
from controller.game import start_game
from data import consts
from data.context import context

if __name__ == "__main__":
    gpc_cred_loc = os.getenv(consts.GOOGLE_APPLICATION_CREDS, os.getcwd() + r'\creds.json')
    if os.path.isfile(gpc_cred_loc):
        os.environ[consts.GOOGLE_APPLICATION_CREDS] = gpc_cred_loc
        context.use_gcp = True
    else:
        print("Missing GCP credentials file:", gpc_cred_loc)
        print("Defaulting to gTTS")
        context.use_gcp = False
    new_listener().start()
    start_game()
