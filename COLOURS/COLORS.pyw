import pygame, pygame.gfxdraw
from pygame.font import Font

pygame.init()
done = False

dim = pygame.display.Info()
# screen = pygame.display.set_mode([dim.current_w, dim.current_h], pygame.FULLSCREEN)
screen = pygame.display.set_mode([720, 480])
pygame.display.set_caption('Colour Picker')
clock = pygame.time.Clock()

RED = (216, 7, 4)
GREEN = (11, 181, 5)
BLUE = (5, 76, 198)
colour = (0, 0, 0)
mainfont = Font('TCM_____.TTF', 25)

class Slider:
    def __init__(self, colour, x, y):
        self.bar = pygame.image.load('slider.png')
        self.rect = self.bar.get_rect()
        self.rect.x, self.rect.y = x, y
        self.colour = colour
        self.x = x
        self.held = False
        self.value = 0
        
    def eventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print('DOWN')
            if self.rect.collidepoint(event.pos):
                self.held = True
                # print(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.held = False
            # print(False)
        if self.held is True:
            if event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                # print(x)
                if x >= (self.rect.x+100):
                    self.x = self.rect.x + 100
                elif x <= self.rect.x:
                    self.x = self.rect.x
                else:
                    self.x = x
        self.checkColour()
    
    def draw(self, screen):
        screen.blit(self.bar, [self.rect.x, self.rect.y])
        pygame.draw.circle(screen, self.colour, (self.x, self.rect.y+12), 8)
        
    def checkColour(self):
        self.value = translate(self.x, self.rect.x, self.rect.x+100, 0, 255)
        

ir = Slider(RED, 45, 35)
ig = Slider(GREEN, 45, 70)
ib = Slider(BLUE, 45, 105)
l_i = [ir, ig, ib]


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def fillScreen(colour):
    screen.fill((l_i[0].value, l_i[1].value, l_i[2].value))
    pygame.gfxdraw.box(screen, pygame.Rect(25, 25, 190, 115), (232, 234, 201, 100))
    

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        for _ in l_i:
            _.eventUpdate(event)
    
    fillScreen(colour)
    
    for _ in l_i:
        _.draw(screen)
        n = round(_.value)
        x = mainfont.render(str(n), True, (0, 0, 0))
        screen.blit(x, [_.rect.x+110, _.rect.y])
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()