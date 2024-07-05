import random

import pygame

from game import Game


class SingleplayerGame(Game):

    def __init__(self, w, h, username='unknown'):
        super().__init__(w, h, username)

        # Always set main player controls
        self.pid = 1
        self.stop_period = 0
        self.difficulty = 0.005

    def run(self):
        super().run()

    def update(self):
        self.reset()
        # self.player2.height = 200
        self.follow_ball_with_center_wait(self.player2)
        self.predict_ball(self.player, draw_lines=True)

    def do_with_stops(self, player, move_function):
        # initialize random stops and not move the paddle within stop periods
        if random.random() < self.difficulty and self.stop_period <= 0:
            self.stop_period = random.random() * 100
        elif self.stop_period > 0:
            self.stop_period -= 1
        else:
            move_function(player)

    @staticmethod
    def follow(player, target_y):
        # round the target variable to prevent jittering
        pv = player.velocity
        target_y = target_y//pv*pv

        # if the player is below the target, move up
        # if below, move down
        player_y = player.get_hitbox().centery
        if player_y > target_y:
            player.move(0)
        elif player_y < target_y:
            player.move(1)

    def follow_ball(self, player):
        self.follow(player, self.ball.y)

    def follow_ball_with_center_wait(self, player):
        player_y = player.get_hitbox().centery
        player_left = player.x < self.width/2

        # if the ball is in the other half, move paddle to the center
        if (player_left and self.ball.x > self.width / 2) or (not player_left and self.ball.x < self.width / 2):
            if player_y > self.height / 2:
                player.move(0)
            elif player_y < self.height / 2:
                player.move(1)
        else:
            self.follow_ball(player)

    def predict_ball(self, player, draw_lines=False):
        player_x = player.x
        if player_x < self.width/2:
            player_x += player.width
        else:
            player_x -= player.width

        slope = 1 if self.ball.vx == 0 else self.ball.vy / self.ball.vx
        target_y = self.ball.y - slope * (self.ball.x - player_x)

        # ball is about to hit the top
        # calculate bounce point and recalculate the target y position
        bounce = (self.ball.x, self.ball.y)
        if target_y < 0:
            bounce = (self.ball.x - self.ball.y / slope, 0)
            target_y = slope * (bounce[0] - player_x)
        elif target_y > self.height:
            bounce = (self.ball.x + (self.height - self.ball.y) / slope, self.height)
            target_y = self.height + slope * (bounce[0] - player_x)

        if draw_lines:
            pygame.draw.line(self.canvas.get_canvas(), (200, 0, 0), (self.ball.x, self.ball.y), bounce)
            pygame.draw.line(self.canvas.get_canvas(), (200, 0, 0), bounce, (player_x, target_y))

        # make the paddle follow the target
        self.follow(player, target_y)

    def big_paddle(self, player):
        player.height = self.width
        player.y = 0


