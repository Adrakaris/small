import pygame

class Slider:
    """
    A slider used for sliding around. The sliderlength depends on the back bar
    slider image. To use, click on the bar, or drag on the bar. The slider will
    follow the mouse. The values are NOT ROUNDED, and must be rounded in post
    if necessary. 
    """
    def __init__(self, icolour, x, y, minval, maxval):
        self.bar = pygame.image.load('slider.png')
        self.rect = self.bar.get_rect()
        self.rect.x, self.rect.y = x, y
        self.colour = icolour
        self.x = x
        self.held = False
        self.value = 0
        self.minval, self.maxval = minval, maxval
        
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

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
        self.checkValue()
    
    def draw(self, screen):
        screen.blit(self.bar, [self.rect.x, self.rect.y])
        pygame.draw.circle(screen, self.colour, (self.x, self.rect.y+12), 8)
        
    def checkValue(self):
        self.value = self.translate(self.x, self.rect.x, self.rect.x+100, self.maxval, self.maxval)
