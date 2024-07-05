from game import Game
from network import Network


class MultiplayerGame(Game):

    def __init__(self, w, h, username='unknown'):
        self.net = Network()

        # get the player ID
        self.pid = int(self.net.id) + 1

        super().__init__(w, h, username)

    def position_players(self, left_player, right_player):
        if self.pid == 1:
            return left_player, right_player
        if self.pid == 2:
            return right_player, left_player

    def run(self):
        super().run()

    def update(self):
        # server communication
        server_reply = self.send_data()
        data = self.parse_data(server_reply)

        self.player2.y = data[1]
        # update ball and score of player 2 screen
        if self.pid == 2:
            self.ball.x = data[2]
            self.ball.y = data[3]
            self.score = int(data[4])
            self.score2 = int(data[5])

    # send formatted data to the server and receive a reply
    def send_data(self):
        data = f"{self.net.id};{self.player.y};{self.ball.x};{self.ball.y};{self.score};{self.score2}"
        reply = self.net.send(data)
        return reply

    # convert the server reply to usable floats
    @staticmethod
    def parse_data(data):
        try:
            d = data.split(";")

            return [float(x) for x in d]
        except:
            return [0, -1000, 0, 0, 0, 0]