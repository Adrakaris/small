# circle drawer adder

import pygame
import math
from inputbox import InputBox
from buttons import Switch
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

# screen size
width, height = 960, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Waveform Adder')
clock = pygame.time.Clock()
mainfont = Font('TCM_____.TTF', 20)

# get stuff for dot
DOTPOINT = pygame.Surface((1, 1))
pygame.gfxdraw.pixel(DOTPOINT, 1, 1, BLACK)


class Dot(pygame.sprite.Sprite):
    """
    Create a constantly moving dot that will plot a point on a cartesian graph

    :param aty: int
        the y coordinate of the point the dot is placing.
    """
    def __init__(self, aty):
        super(Dot, self).__init__()
        self.image = DOTPOINT  # dotpoint is a 1*1 pixel dot
        self.rect = self.image.get_rect()
        self.rect.x = 360  # start 
        self.rect.y = aty  # constant y position

    def update(self):
        """move self across by 1 every tick"""
        self.rect.x += 1
        if self.rect.x > 720:  # destroy self at end of graph
            self.kill()


class Drawer(pygame.sprite.Sprite):
    def __init__(self, n, it):
        super(Drawer, self).__init__()
        self.it = it  # iteration to track positions
        self.n = n  # to track number, as string
        self.crx = 180  # circle is positioned that centre x = 180 and y = 240
        self.cry = 240  # initialise cartesian coordinates to 90 deg
        self.rad = 160  # assign circle radius
        self.ang = math.radians(90)  # associate with pi by 2
        self.x, self.y = 0, 0  # initialise blank true x and y coords
        self.speed = 1  # initialise speed as 1 that can be changed
        # create relevant text boxes
        self.SW = mainfont.render('WAVEFORM ' + self.n, True, BLACK)
        self.SP = mainfont.render('SPEED', True, BLACK)  # text
        self.SZ = mainfont.render('SIZE', True, BLACK)  # text
        self.box_SP = InputBox(screen=screen, x=820, y=self.it[1][1], w=120, h=20,
                               fftf=mainfont, text=str(self.speed))
        self.box_SZ = InputBox(screen=screen, x=820, y=self.it[2][1], w=120, h=20,
                               fftf=mainfont, text=str(self.rad))

    def drawbox(self, screen):
        """Draws all configuration boxes and context text"""
        screen.blit(self.SW, self.it[0])
        screen.blit(self.SP, self.it[1])
        screen.blit(self.SZ, self.it[2])
        self.box_SP.draw()
        self.box_SZ.draw()
    
    def update(self, event):
        self.box_SP.eventUpdate(event)
        self.box_SZ.eventUpdate(event)
        self.box_SP.update()
        self.box_SZ.update()
        try:
            self.speed = int(self.box_SP.text)
        except ValueError:
            pass
        try:
            self.rad = int(self.box_SZ.text)
        except ValueError:
            pass

    def draw(self, screen):
        self.drawbox(screen)
        pygame.gfxdraw.aacircle(screen, 180, 240, self.rad, BLACK)  # draw circle
        # find true x and y coords based on relative polar coords
        self.x = self.crx + self.rad * math.cos(self.ang)  
        self.y = self.cry - self.rad * math.sin(self.ang)
        # draw the circle representing the drawer
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 5, RED)

        # change angle, moving clockwise so go backwards radians - this is
        # just for effect as the same curve would be produced with an anticlockwise
        # moving drawer.
        self.ang -= math.radians(self.speed)

        return self.y  # returns the y value so it can be added up and modulated


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def modulate(values):
    """
    Modulates the wave based on the number of values and index.

    :param values: 1d array
        Takes in all the raw values as data and modulates them to one waveform.
    """
    modval = []
    # shift everything in a ratio
    for value in values:
        tr = translate(value, 80, 400, -1, 1)
        modval.append(tr)
    if len(modval) != 0:
        total = sum(modval)  # average all the floats
        oval = translate(total, -len(values), len(values), 80, 400)  # coalesce into final num
    else:
        oval = 240
    return oval


# creation of all buttons
b1 = Switch(image_off='soff.png', image_on='son.png', x=40, y=440)
b2 = Switch(image_off='soff.png', image_on='son.png', x=200, y=440)
b3 = Switch(image_off='soff.png', image_on='son.png', x=360, y=440)
b4 = Switch(image_off='soff.png', image_on='son.png', x=520, y=440)
buttons = [b1, b2, b3, b4]
# creation of all circles
d1 = Drawer(n='01', it=[[740, 20], [740, 50], [740, 80]])
d2 = Drawer(n='02', it=[[740, 140], [740, 170], [740, 200]])
d3 = Drawer(n='03', it=[[740, 270], [740, 300], [740, 330]])
d4 = Drawer(n='04', it=[[740, 400], [740, 430], [740, 460]])
drawers = [d1, d2, d3, d4]

waveform = pygame.sprite.Group()

# main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit program

        for button in buttons:
            button.update(event)  # update every button
            
        for lm in drawers:
            lm.update(event)  # update every drawer

    # displ draw and fill
    screen.fill(WHITE)
    for button in buttons:
        button.draw(screen)

    # draw graph
    pygame.gfxdraw.hline(screen, 360, 720, 240, (155, 155, 155))
    pygame.gfxdraw.hline(screen, 360, 720, 160, GREY)
    pygame.gfxdraw.hline(screen, 360, 720, 320, GREY)
    pygame.gfxdraw.vline(screen, 360, 80, 400, BLACK)

    # logic for drawing drawers and retrieving values
    outvalues = []
    for b in range(len(buttons)):
        # for every button, if that button is green, on, draw the corresponding
        # circle drawer for that button. Otherwise, hide it and do nothing.
        if buttons[b].toggle:  
            v = drawers[b].draw(screen)
            outvalues.append(v)  # retrieve and append the y values
        else:
            pass

    # logic for getting a line in
    mv = modulate(outvalues)
    # print(mv)
    dot = Dot(mv)
    waveform.add(dot)
    waveform.update()
    waveform.draw(screen)

    # end
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
