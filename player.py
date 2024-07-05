import pygame


class Player:
    width = 20
    height = 80
    velocity = 3

    def __init__(self, startx, starty, screenw, screenh, color=(255, 255, 255)):
        self.x = startx
        self.y = starty
        self.screenw = screenw
        self.screenh = screenh
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color, self.get_hitbox(), 0)

    def move(self, dirn):
        if dirn == 0 and self.y >= 0:
            self.y -= self.velocity
        elif dirn == 1 and self.y <= self.screenh - self.height:
            self.y += self.velocity

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
