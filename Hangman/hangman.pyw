import pygame, random
from pygame.font import Font

# initialise pygame
pygame.init()
done = False

# define colours
BLACK = (0, 0, 0)
LGREY = (215, 215, 215)
WHITE = (255, 255, 255)
RED = (226, 13, 13)

# define screen size
width, height = 720, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
mainfont = Font('TCM_____.TTF', 48)

# get words
file = open('words.txt', 'r')
words = []
for i in file:
    words.append(i[:-1])
file.close()
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class Button(pygame.sprite.Sprite):
    """
    Create a clickable button with an image from a file.
    Used for things like enter, give up, new game, etc.
    """
    def __init__(self, image, cast):
        super(Button, self).__init__()
        self.imgname = image
        self.image = pygame.image.load(self.imgname)
        self.cast = cast
        self.rect = self.image.get_rect()

    def eventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # print('>>> I, %s have been clicked' % self.imgname)
                self.activate(self.cast)

    def activate(self, func):
        """ Activates the relevant function """
        if func == 'new':
            hangman.newgame(random.choice(words))
        elif func == 'enter':
            if submit.text.lower() in letters:
                hangman.isinlist(submit.text)
                submit.text = ''
            else:
                pass
        elif func == 'fail':
            hangman.lives = 0
            hangman.isinlist(';')


class Input:
    """
    create input box with dimensions, and text.
    This input box will input a letter.
    """
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h) # create pygame.rectangle with dimensions
        self.active = True # redundancy
        self.color = LGREY
        self.text = text
        self.txt_surface = mainfont.render(text, True, BLACK) # uses the Tw Cen MT font

    def eventUpdate(self, event): # self update for EVENTS, check if clicked on
        if event.type == pygame.KEYDOWN: # if active and a key is pressed; a key usually returns a unicode code
            if self.active:
                if event.key == pygame.K_RETURN: # if ENTER is pressed, activate.
                    buttons[2].activate(buttons[2].cast)
                    self.text = ''
                    pass
                elif event.key == pygame.K_BACKSPACE: # if BACKSPACE is pressed, remove all character
                    self.text = ''
                else:
                    self.text = event.unicode # else bang character into text field
                self.txt_surface = mainfont.render(self.text, True, BLACK) # render text

    def update(self): # self update size
        width = max(48, self.txt_surface.get_width() + 5) # if text is longer than box, extend box
        self.rect.w = width

    def draw(self, screen): # draw input field as rect
        pygame.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.txt_surface, [self.rect.x+5, self.rect.y-3]) # align text
        
    def addtext(self): # just update the bloody text
        self.txt_surface = mainfont.render(self.text, True, BLACK)
        screen.blit(self.txt_surface, [(self.rect.x+10), (self.rect.y-3)])


class TextBox:
    """Create a single letter box to make a letter displayed ja"""
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LGREY
        self.text = text
        self.txt_surface = mainfont.render(text, True, RED)
        self.empty = True
    
    def update(self):
        self.rect.w = max(48, self.txt_surface.get_width() + 5)
        if self.text != '':
            self.empty = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        self.txt_surface = mainfont.render(self.text, True, RED)
        screen.blit(self.txt_surface, [(self.rect.x+10), (self.rect.y-3)])


class Hangman:
    """
    The main text class, which will update accoding to the input field
    There will be 6 images, this will be sorted in the update class.
    The image dimensions will be 140 * 200 and will be set at 20, 20.
    """
    def __init__(self, text):
        self.text = text
        self.textlist = list(text.lower())
        self.lives = 6
        self.image = pygame.image.load('hmplaceholder.png') # starting image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 20, 20
        self.blank = []
        self.blankstr = ''
        self.colour = BLACK
        self.losting = False
        self.winsting = False
        # print(text)
        
        for i in self.textlist:
            self.blank.append('_')
        for i in self.blank:
            self.blankstr += (i + ' ')

    def newgame(self, text):
        self.winsting = False
        self.losting = False
        self.blank = []
        self.blankstr = ''
        self.colour = BLACK
        self.text = text
        self.textlist = list(text.lower())
        self.lives = 6
        # print(text)
        
        for box in xboxes:
            box.text = ''
        
        for i in self.textlist:
            self.blank.append('_')
        for i in self.blank:
            self.blankstr += (i + ' ')
            
    def imagedraw(self):
        if self.losting is True:
            l = 'sd.png'
        elif self.winsting is True:
            l = 'sw.png'
        else:
            if self.lives == 6:
                l = 's0.png'
            elif self.lives == 5:
                l = 's1.png'
            elif self.lives == 4:
                l = 's2.png'
            elif self.lives == 3:
                l = 's3.png'
            elif self.lives == 2:
                l = 's4.png'
            elif self.lives == 1:
                l = 's5.png'
            elif self.lives == 0:
                l = 's6.png'
            else:
                l = 'hmplaceholder.png'
        return pygame.image.load(l)

    def draw(self, screen):
        # draw picture in here
        self.blankstr = ''
        for i in self.blank:
            self.blankstr += (i + ' ')
        # draw unknown text
        livestext = ("LIVES REMAINING: %s" % self.lives)
        livessurface = mainfont.render(livestext, True, self.colour)
        screen.blit(self.imagedraw(), self.rect)
        blanksurface = Font('TCM_____.TTF', 48).render(self.blankstr, True, self.colour)
        screen.blit(blanksurface, [180, 20])
        screen.blit(livessurface, [20, 232])
        
        if self.blank == self.textlist and self.lives >= 0:
            self.winsting = True
            wintext = Font('TCM_____.TTF', 36).render('You Win!', True, self.colour)
            screen.blit(wintext, [180, 70])

    def isinlist(self, letter):
        if self.lives >= 0:
            if letter.lower() in self.textlist:
                for i in range(len(self.textlist)):
                    if letter.lower() == self.textlist[i]:
                        self.blank[i] = letter.lower()
            elif letter.lower() not in self.textlist:
                if self.lives == 0:
                    for i in range(len(self.textlist)):
                        self.blank[i] = self.textlist[i]
                    self.colour = RED
                    self.losting = True
                else:
                    self.lives -= 1
                    for b in xboxes:
                        if b.empty is True:
                            b.text = letter.upper()
                            break
        elif self.winsting is True:
            pass
        else:
            for i in range(len(self.textlist)):
                self.blank[i] = self.textlist[i]
            self.colour = RED
            self.losting = True


# title font and text lines
tfont = Font('TCM_____.TTF', 48)
f_list = [['NEW GAME', 24],
          ['GIVE UP', 24],
          ['ENTER', 24]]

# create buttons and boxes
new = Button('new.png', 'new'); new.rect.x, new.rect.y = 248, 300
fail = Button('fail.png', 'fail'); fail.rect.x, fail.rect.y = 248, 368
enter = Button('enter.png', 'enter'); enter.rect.x, enter.rect.y = 248, 172
buttons = [new, fail, enter]
submit = Input(180, 172, 48, 48)
l1 = TextBox(20, 300, 48, 48)
l2 = TextBox(20+68, 300, 48, 48)
l3 = TextBox(20+68+68, 300, 48, 48)
l4 = TextBox(20, 368, 48, 48)
l5 = TextBox(20+68, 368, 48, 48)
l6 = TextBox(20+68+68, 368, 48, 48)
xboxes = [l1, l2, l3, l4, l5, l6]
hangman = Hangman(random.choice(words))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # check quit
            done = True
        # if event.type == pygame.MOUSEMOTION:
            # a = pygame.mouse.get_pos()
            # print('Mouse Position', a)
        submit.eventUpdate(event)
        for button in buttons:
            button.eventUpdate(event)

    # disp text fill
    screen.fill(WHITE)
    hangman.draw(screen)
    
    for button in buttons:
        screen.blit(button.image, button.rect)

    lenter = Font('TCM_____.TTF', 48).render('Attempt', True, BLACK)
    screen.blit(lenter, [310, 172])
    lfail = Font('TCM_____.TTF', 48).render('Give Up', True, BLACK)
    screen.blit(lfail, [310, 368])
    lnew = Font('TCM_____.TTF', 48).render('New Game', True, BLACK)
    screen.blit(lnew, [310, 300])

    submit.update()
    submit.draw(screen)
    
    for box in xboxes:
        box.update()
    for box in xboxes:
        box.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
