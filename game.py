import pygame
from ball import Ball
from network import Network
from player import Player

gray = (100, 100, 100)


class Game:
    # 0 - pocetak, 1 - player1, 2 - player2
    touch_side = 0  # prevencija da lopta udari igraca dva puta
    pid = 0  # player id

    def __init__(self, w, h, username):
        self.net = Network()
        # PlayerID za rad sa serverom
        self.pid = int(self.net.id) + 1

        # username koji dobijamo logovanjem
        self.username = username

        self.width = w
        self.height = h
        border = 50
        pl_height = h / 2 - Player.height / 2

        self.score = self.score2 = 0

        left_player = Player(border, pl_height, w, h)
        right_player = Player(w - border - Player.width, pl_height, w, h)

        if self.pid == 1:
            self.player = left_player
            self.player2 = right_player
        if self.pid == 2:
            self.player2 = left_player
            self.player = right_player

        self.ball = Ball(w, h)
        self.canvas = Canvas(self.width, self.height, "RMT PONG")

    def run(self):
        global gray

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(200)

            # EVENT LOOP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                run = False

            if keys[pygame.K_SPACE]:
                self.touch_side = 0
                if self.pid == 1:
                    self.ball.start()

            if keys[pygame.K_UP]:
                self.player.move(0)

            if keys[pygame.K_DOWN]:
                self.player.move(1)

            # update lopte, update score-a (vrsi player 1)
            if self.pid == 1:
                result = self.ball.move()
                if result == 1:
                    self.score2 += 1
                if result == 2:
                    self.score += 1

            # kolizija lopte i igraca
            if self.ball.get_hitbox().colliderect(self.player.get_hitbox()) and self.touch_side != 2:
                self.touch_side = 2
                self.ball.touch_player()
            if self.ball.get_hitbox().colliderect(self.player2.get_hitbox()) and self.touch_side != 1:
                self.touch_side = 1
                self.ball.touch_player()

            # Komunikacija sa serverom
            server_reply = self.send_data()
            data = self.parse_data(server_reply)
            self.player2.y = data[1]
            # drugi igrac cita polozaj lopte koju racuna prvi igrac
            if self.pid == 2:
                self.ball.x = data[2]
                self.ball.y = data[3]
                self.score = int(data[4])
                self.score2 = int(data[5])

            # Rendering
            self.canvas.draw_background()
            pygame.draw.line(self.canvas.get_canvas(), gray, (self.width / 2, 0), (self.width / 2, self.height))

            self.canvas.draw_text(self.username, 30, 0, 0)

            self.canvas.draw_text(str(self.score), 72, self.width / 4, 40)
            self.canvas.draw_text(str(self.score2), 72, 3 * self.width / 4 - 36, 40)

            if self.pid == 1:
                self.canvas.draw_text("player 1", 32, 0, self.height - 48)
            else:
                self.canvas.draw_text("player 2", 32, self.width - 125, self.height - 48)

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        format poruke: ID; player.y; ball.x; ball.y; score; score 2 
        """
        data = "{0};{1};{2};{3};{4};{5}".format(str(self.net.id), str(self.player.y), str(self.ball.x),
                                                str(self.ball.y), str(self.score), str(self.score2))

        reply = self.net.send(data)
        return reply

    # vraca listu float od stringa
    @staticmethod
    def parse_data(data):
        try:
            d = data.split(";")

            return [float(x) for x in d]
        except:
            return [0, -1000, 0, 0, 0, 0]


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        global gray
        pygame.font.init()
        font = pygame.font.SysFont("Consolas", size)
        render = font.render(text, 1, gray)
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))
