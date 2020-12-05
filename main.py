from clients.keyboard import new_listener
from controller.game import start_game

if __name__ == "__main__":
    new_listener().start()
    start_game()
