from game import Game
from login import MainScreen
from multiplayer_game import MultiplayerGame
from singleplayer_game import SingleplayerGame

if __name__ == "__main__":
    ms = MainScreen()
    ms.run()
    g = Game(800, 600)
    # Pritiskom na play, prozor se gasi i samim tim zavrsava fja run
    if ms.game_running:
        if ms.mode == 'player':
            g = MultiplayerGame(800, 600, username=ms.logged_user)
        else:
            g = SingleplayerGame(800, 600, username=ms.logged_user or 'guest')
        g.run()

        ms.on_exit()

