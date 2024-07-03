from game import Game
from login import MainScreen

# if __name__ == "__main__":
#     ms = MainScreen()
#     ms.run()
#     # Pritiskom na play, prozor se gasi i samim tim zavrsava fja run
#     if ms.game_running:
#         g = Game(800, 600, ms.logged_user)
#         g.run()
#
#         ms.on_exit()

if __name__ == "__main__":
    g = Game(800, 600, 'test')
    g.run()
