import pygame
import random
from network import Network


class Player():
    width = 20
    height = 100

    def __init__(self, startx, starty, screenw, screenh, color=(255,255,255)):
        self.x = startx
        self.y = starty
        self.screenw = screenw
        self.screenh = screenh
        self.color = color
        self.reset()

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def reset(self):
        self.velocity = 2

    def move(self, dirn):
        self.velocity *= 1.03
        if dirn == 0 and self.y >= 0:
            self.y -= self.velocity
        elif dirn == 1 and self.y <= self.screenh-self.height:
            self.y += self.velocity

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Ball():
    r = 15
    flash = 0
    vx = vy = 0

    def __init__(self, screenw, screenh, color=(255,255,255)):
        self.screenw = screenw
        self.screenh = screenh
        self.color = color
        self.reset()

    # ako je flash pokrenut (>0) i lopta je u centru, menjaj boju
    def draw(self, g):
        if self.flash > 0 and (self.x == self.screenw/2 and self.y == self.screenh/2):
            self.flash += 1
            val = 200 - self.flash%150
            self.color=(val, val, val)
        else:
            self.color=(255, 255, 255)

        pygame.draw.circle(g, self.color, (self.x,self.y), self.r, 0)
        

    # prekid: stavi loptu u centar, pokreni flash animaciju
    def reset(self):
        self.x = self.screenw/2
        self.y = self.screenh/2
        
        self.flash = 1

    # pocetak nakon prekida: odredi random smer lopte, zaustavi flash
    def start(self):
        if self.x == self.screenw/2 and self.y == self.screenh/2:
            sign = 1 if random.random() > 0.5 else -1
            self.vx = sign*(2 + random.random())
            sign = 1 if random.random() > 0.5 else -1
            self.vy = sign*(2 + random.random())

        self.flash = 0
        return self.vx, self.vy


    def move(self):
        # ako je flash iskljucen pomeri loptu
        if (self.flash == 0):
            self.x += self.vx
            self.y += self.vy

        # udarac u gornju/donju ivicu 
        if (self.y-self.r <= 0 or self.y+self.r >= self.screenh):
            self.vy *= -1

        # udarac u levu/desnu stranu, lopta se resetuje
        # fja vraca se 1 ili 2 ako je lopta dotakla levu/desnu stranu
        if (self.x+self.r <= 0):
            self.reset()
            return 1
        elif (self.x-self.r >= self.screenw):
            self.reset()
            return 2
        else: 
            return 0

    def touch_player(self):
        self.vx *= -1

    def get_hitbox(self):
        return pygame.Rect(self.x-self.r, self.y-self.r, 2*self.r, 2*self.r)



gray = (100, 100, 100)
class Game:

    # 0 - pocetak, 1 - player1, 2 - player2
    touch_side = 0 # prevencija da lopta udari igraca dva puta
    pid = 0 # player id
    

    def __init__(self, w, h, username):
        self.net = Network()
        # PlayerID za rad sa serverom
        self.pid = int(self.net.id) + 1

        # username koji dobijamo logovanjem
        self.username = username

        self.width = w
        self.height = h
        border = 50
        plheight = h/2-Player.height/2

        self.score = self.score2 = 0

        if (self.pid == 1):
            self.player = Player(border, plheight, w, h)
            self.player2 = Player(w-border-Player.width, plheight, w, h)
        if (self.pid == 2):
            self.player2 = Player(border, plheight, w, h)
            self.player = Player(w-border-Player.width, plheight, w, h)
        

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

                if event.type == pygame.KEYUP:
                    self.player.reset()

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
            if (self.pid == 1):
                result = self.ball.move()
                if (result == 1):
                    self.score2 += 1
                if (result == 2):
                    self.score += 1

            # kolizija lopte i igraca
            if (self.ball.get_hitbox().colliderect(self.player.get_hitbox()) and self.touch_side != 2):
                self.touch_side = 2
                self.ball.touch_player()
            if (self.ball.get_hitbox().colliderect(self.player2.get_hitbox()) and self.touch_side != 1):
                self.touch_side = 1
                self.ball.touch_player()


            # Komunikacija sa serverom
            server_reply = self.send_data()
            data = self.parse_data(server_reply)
            self.player2.y = data[1]
            # drugi igrac cita polozaj lopte koju racuna prvi igrac
            if (self.pid == 2):
                self.ball.x = data[2]
                self.ball.y = data[3]
                self.score  = int(data[4])
                self.score2 = int(data[5])


            # Rendering
            self.canvas.draw_background()
            pygame.draw.line(self.canvas.get_canvas(), gray, (self.width/2,0), (self.width/2,self.height))

            self.canvas.draw_text(self.username, 30, 0, 0)

            self.canvas.draw_text(str(self.score),  72, self.width/4, 40)
            self.canvas.draw_text(str(self.score2), 72, 3*self.width/4-36, 40)

            if (self.pid == 1):
                self.canvas.draw_text("player 1", 32, 0, self.height-48)
            else:
                self.canvas.draw_text("player 2", 32, self.width - 125, self.height-48)

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()


    def send_data(self):
        """
        format poruke: ID; player.y; ball.x; ball.y; score; score 2 
        """
        data =  str(self.net.id) + ";" + \
                str(self.player.y) + ";" + \
                str(self.ball.x) + ";" + str(self.ball.y) + ";" + \
                str(self.score) + ";" + str(self.score2)

        reply = self.net.send(data)
        return reply

    # vraca listu float od stringa
    @staticmethod
    def parse_data(data):
        try:
            d = data.split(";")
            
            return [float(x) for x in d] 
        except:
            return [0,-1000,0,0,0,0]


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        global gray
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, gray)
        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0,0,0))
