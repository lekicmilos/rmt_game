import random

import pygame
from ball import Ball
from network import Network
from player import Player

gray = (100, 100, 100)


class Game:
    # 0 - pocetak, 1 - player1, 2 - player2
    touch_side = 0  # prevencija da lopta udari igraca dva puta
    pid = 0  # player id

    def __init__(self, w=0, h=0, username='unknown'):
        """
        :param w: screen width
        :param h: screen height
        """
        self.username = username
        self.width = w
        self.height = h

        border = 50
        pl_height = h / 2 - Player.height / 2

        self.score = self.score2 = 0

        left_player = Player(border, pl_height, w, h)
        right_player = Player(w - border - Player.width, pl_height, w, h)

        self.player, self.player2 = self.position_players(left_player, right_player)

        self.ball = Ball(w, h)
        self.canvas = Canvas(self.width, self.height, "RMT PONG")

    def run(self):
        global gray

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(200)
            self.canvas.draw_background()
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                run = False

            if keys[pygame.K_SPACE]:
                self.reset()

            if keys[pygame.K_UP]:
                self.player.move(0)

            if keys[pygame.K_DOWN]:
                self.player.move(1)

            # ball and player collision
            if self.ball.get_hitbox().colliderect(self.player.get_hitbox()) and self.touch_side != 2:
                self.touch_side = 2
                self.ball.touch_player()
            if self.ball.get_hitbox().colliderect(self.player2.get_hitbox()) and self.touch_side != 1:
                self.touch_side = 1
                self.ball.touch_player()

            # update the ball and the score of player 1 screen
            if self.pid == 1:
                result = self.ball.move()
                if result == 1:
                    self.score2 += 1
                if result == 2:
                    self.score += 1

            # update the enemy paddle and game state for player 2
            self.update()

            # Rendering
            # self.canvas.draw_background()
            pygame.draw.line(self.canvas.get_canvas(), gray, (self.width / 2, 0), (self.width / 2, self.height))
            # self.canvas.draw_text(self.username, 30, 0, 0)
            self.canvas.draw_text(f"v: {round(self.ball.vx,2)} ", 20, 0, 0)
            self.canvas.draw_text(f"{round(self.ball.vy,2)} ", 20, 100, 0)

            self.canvas.draw_text(str(self.score), 72, self.width / 4, 40)
            self.canvas.draw_text(str(self.score2), 72, 3 * self.width / 4 - 36, 40)

            if self.pid == 1:
                self.canvas.draw_text("player 1", 32, 0, self.height - 48)
            else:
                self.canvas.draw_text("player 2", 32, self.width - 150, self.height - 48)

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def position_players(self, left_player, right_player):
        return left_player, right_player

    def update(self):
        pass

    def reset(self):
        if self.pid and self.ball.x == self.width / 2 and self.ball.y == self.height / 2:
            self.touch_side = 0
            self.ball.start()


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y, color=gray):
        global gray
        pygame.font.init()
        font = pygame.font.SysFont("Consolas", size)
        render = font.render(text, 1, color)
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))
