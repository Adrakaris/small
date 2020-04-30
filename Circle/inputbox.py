import pygame


class InputBox:
    """
    An input box for a pygame UI.
    Is used to store plain text.
    
    Parameters
    ----------
    screen : pygame.display object
        The screen to place the input box on and render to.
    
    x, y : int
        The x and y coordinate placements for the TOP LEFT of the box.
        
    w, h : int
        w, the minimum width of the text box.
        h, the height of the text box. Ideally should be the exact height of the font.
        
    fftf : pygame.font.Font object
        The Font that will be displayed in the text box. Different fonts may require adjustment.
    
    fontadj : int, optional (default=3)
        The font offset from the corner of the text box. This is to ensure that the text is drawn
        in a clean manner that does not look misaligned. The default 3 is true for the Twentieth
        Century MT Normal font.
        
    text : str, optional (default='')
        The text will be displayed and updated at every frame. This is the initial text contained
        in the text box. It is not reccomended to change this upon init, but can be used for
        inserting error messages into output boxes.
        
    deselect : tuple, optional (default=(235, 235, 235))
        Three integer tuple ranging from 0-255 each. Determines the deselected colour that the text
        box uses. The default for this is light grey.
        
    select : tuple, optional (default=(215, 215, 215))
        Three integer tuple ranging from 0-255 each. Determines the selected colour that the text
        box uses. The default for this is a slightly darker light grey.
        
    fcol : tuple, optional (default=(0, 0, 0))
        Three integer tuple ranging from 0-255 each. Determines the colour used to display the font
        in the text box. A suitable colour against the background colours should be chosen. The
        default is black.
    """
    def __init__(self, screen, x, y, w, h, fftf, text='', fontadj=3,
                 deselect=(235, 235, 235), select=(215, 215, 215), fcol=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, w, h)  # create pygame.rectangle with dimensions
        self.active = False  # for toggling input on the box
        self.LGREY = deselect
        self.DrGREY = select
        self.color = deselect
        self.BLACK = fcol
        self.text = text
        self.fftf = fftf
        self.screen = screen
        self.fontadj = fontadj
        self.txt_surface = fftf.render(text, True, self.BLACK)  # uses the main font

    def eventUpdate(self, event):  # self update for EVENTS, check if clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print('>>> Clicked on!')
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # toggles active status
            else:
                self.active = False
            self.color = self.DrGREY if self.active else self.LGREY
            # either darkens or lightens the input box depending on toggle
        if event.type == pygame.KEYDOWN:  # if active and a key is pressed; a key usually returns a unicode code
            if self.active:
                if event.key == pygame.K_RETURN:  # if ENTER is pressed, print contents to console. DEBUG PURPOSES
                    print('Enter pressed. Contents:', self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:  # if BACKSPACE is pressed, remove character
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # else add character to text field
                self.txt_surface = self.fftf.render(self.text, True, self.BLACK)  # render text

    def update(self):  # self update size
        width = max(200, self.txt_surface.get_width() + 10)  # if text is longer than box, extend box
        self.rect.w = width

    def draw(self):  # draw input field as rect
        pygame.draw.rect(self.screen, self.color, self.rect, 0)
        self.screen.blit(self.txt_surface, [self.rect.x+self.fontadj, self.rect.y-self.fontadj])  # align text
        
    def addtext(self):  # just update the bloody text
        self.txt_surface = self.fftf.render(self.text, True, self.BLACK)
        self.screen.blit(self.txt_surface, [self.rect.x+self.fontadj, self.rect.y-self.fontadj])
