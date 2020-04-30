# main circle drawer

import pygame
import math
# from inputbox import InputBox
from pygame.font import Font
from pygame import gfxdraw

# init pygame
pygame.init()
done = False

# define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (226, 13, 13)
GREY = (215, 215, 215)
PI = math.pi

# def screen size
width, height = 960, 540
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
mainfont = Font('TCM_____.TTF', 20)

# get stuff for dot
DOTPOINT = pygame.Surface((1, 1))
pygame.gfxdraw.pixel(DOTPOINT, 1, 1, RED)


class Dot(pygame.sprite.Sprite):  # create a dot object which moves on the screen
    def __init__(self, aty):
        super(Dot, self).__init__()
        self.image = DOTPOINT
        self.rect = self.image.get_rect()
        self.rect.x = 360
        self.rect.y = aty

    def update(self):
        self.rect.x += 1
        if self.rect.x > 720:
            self.kill()


class Drawer:
    def __init__(self):
        self.crx = 180
        self.cry = 240
        self.rad = 160
        self.ang = math.radians(90)
        self.line = pygame.sprite.Group()
        self.x, self.y = 0, 0

    def update(self, screen):
        self.line.update()
        self.line.draw(screen)

    def draw(self, screen):
        self.x = self.crx + self.rad * math.cos(self.ang)
        self.y = self.cry - self.rad * math.sin(self.ang)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 5, RED)

        # create dot
        dot = Dot(self.y)
        self.line.add(dot)

        self.ang -= math.radians(1)
        """
        self.x = self.x + self.rad * math.radians(1) * math.cos(self.ang + PI / 2)
        self.y = self.y - self.rad * math.radians(1) * math.sin(self.ang + PI / 2)
        """ 


drawer = Drawer()
"""
dcrx = 240
dcry = 240
drad = 160
dang = PI/2
dinc = math.radians(1)
"""

# main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # displ draw and fill
    screen.fill(WHITE)
    pygame.gfxdraw.aacircle(screen, 180, 240, 160, BLACK)
    # draw an axis
    pygame.gfxdraw.hline(screen, 360, 720, 240, BLACK)
    pygame.gfxdraw.hline(screen, 360, 720, 160, GREY)
    pygame.gfxdraw.hline(screen, 360, 720, 320, GREY)
    pygame.gfxdraw.vline(screen, 360, 80, 400, BLACK)

    drawer.draw(screen)
    drawer.update(screen)

    """
    # ===================
    # drawer?
    dx = dcrx + drad * math.cos(dang)
    dy = dcry - drad * math.sin(dang)
    pygame.gfxdraw.filled_circle(screen, int(dx), int(dy), 4, RED)
    dang = dang - dinc
    dx = dx + drad * math.cos(dang) * dinc
    dy = dy - drad * math.sin(dang) * dinc
    print(dx, dy)
    # ====================
    """

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
