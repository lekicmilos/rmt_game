import pygame
import random


def abs_increase(v, dv):
    return v + dv if v > 0 else v - dv


class Ball:
    r = 15
    flash = 0
    vx = vy = 0

    def __init__(self, screenw, screenh, color=(255, 255, 255)):
        self.screenw = screenw
        self.screenh = screenh
        self.color = color
        self.reset()

    # ako je flash pokrenut (>0) i lopta je u centru, menjaj boju
    def draw(self, g):
        if self.flash > 0 and (self.x == self.screenw / 2 and self.y == self.screenh / 2):
            self.flash += 1
            val = 200 - self.flash % 150
            self.color = (val, val, val)
        else:
            self.color = (255, 255, 255)

        pygame.draw.circle(g, self.color, (self.x, self.y), self.r, 0)

    # prekid: stavi loptu u centar, pokreni flash animaciju
    def reset(self):
        self.x = self.screenw / 2
        self.y = self.screenh / 2
        print(self.vx, self.vy)
        self.flash = 1

    # pocetak nakon prekida: odredi random smer lopte, zaustavi flash
    def start(self):
        sign = 1 if random.random() > 0.5 else -1
        self.vx = sign * (2 + random.random())
        sign = 1 if random.random() > 0.5 else -1
        self.vy = sign * (2 + random.random())

        self.flash = 0
        return self.vx, self.vy

    def move(self):
        # move the ball, if flash is off
        if not self.flash:
            self.x += self.vx
            self.y += self.vy

        # upper/lower edge bounce
        if self.y - self.r <= 0 or self.y + self.r >= self.screenh:
            # change direction
            self.vy *= -1

        # ball hits the side
        if self.x + self.r <= 0:
            self.reset()
            return 1
        elif self.x - self.r >= self.screenw:
            self.reset()
            return 2
        else:
            return 0

    def touch_player(self):
        # change direction
        self.vx *= -1
        # randomly increase or decrease the horizontal and vertical speed
        self.speed_increase()

    def speed_increase(self):
        d = random.random()
        d_signed = -d if random.random() < 0.2 else d
        # if self.vx < 20:
        self.vx = abs_increase(self.vx, d_signed)

        d = random.random()
        d_signed = -d if random.random() < 0.2 else d
        self.vy = abs_increase(self.vy, d_signed)

    def get_hitbox(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)
