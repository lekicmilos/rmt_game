import pygame
import random


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

        self.flash = 1

    # pocetak nakon prekida: odredi random smer lopte, zaustavi flash
    def start(self):
        if self.x == self.screenw / 2 and self.y == self.screenh / 2:
            sign = 1 if random.random() > 0.5 else -1
            self.vx = sign * (2 + random.random())
            sign = 1 if random.random() > 0.5 else -1
            self.vy = sign * (2 + random.random())

        self.flash = 0
        return self.vx, self.vy

    def move(self):
        # ako je flash iskljucen pomeri loptu
        if self.flash == 0:
            self.x += self.vx
            self.y += self.vy

        # udarac u gornju/donju ivicu
        if self.y - self.r <= 0 or self.y + self.r >= self.screenh:
            self.vy *= -1

        # udarac u levu/desnu stranu, lopta se resetuje
        # fja vraca se 1 ili 2 ako je lopta dotakla levu/desnu stranu
        if self.x + self.r <= 0:
            self.reset()
            return 1
        elif self.x - self.r >= self.screenw:
            self.reset()
            return 2
        else:
            return 0

    def touch_player(self):
        self.vx *= -1

    def get_hitbox(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)
