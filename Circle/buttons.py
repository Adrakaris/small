"""
   BUTTON.py
"""

import pygame


class Button(pygame.sprite.Sprite):
    """
    A button used in pygame UI.
    This can be clicked, which will activate a function.
    The way this button works is it will evaluate a function string, and activate it.
    The return value can be stored in self.ret, but will be overwritten every time the function is activated.

    Parameters
    ----------
    image_up : str
        The name of the image the button takes when it is NOT PRESSED.
        Ensure that the exact image name is given.

    image_down : str
        The name if the image the button takes when it is PRESSED.
        Ensure that the exact image name is given.
        *Important* : Make sure that this image has the SAME RESOLUTION as image_up.

    x, y : int
        The x and y coordinate placements for the TOP LEFT of the button.
        The image dimensions of the switch are used.
        
    func : str
        The function to be executed. This will be executed within the object.
        Please input the EXACT string, as if the function were to be executed. If the function was something like
        execute(), then exactly input 'execute()'. Due to limitations to parse something through a function in this
        please use one consistent variable, and not a data piece.
    """
    def __init__(self, image_up, image_down, x, y, func):
        super(Button, self).__init__()
        self.i_up = image_up
        self.i_down = image_down
        self.image = pygame.image.load(self.i_up)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.func = func  # to record function of button.
        self.ret = None  # return from function

    def update(self, event):
        """
        Updates the button depending on the pygame.event event.
        :param event: pygame.event event
            Please put this update function in the main event loop.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = pygame.image.load(self.i_down)
                self.ret = eval(self.func)
        if event.type == pygame.MOUSEBUTTONUP:
            self.image = pygame.image.load(self.i_up)

    def draw(self, screen):
        """Draw to screen."""
        screen.blit(self.image, self.rect)


class Switch(pygame.sprite.Sprite):
    """
    A toggle switch used in pygame UI.
    This can be toggled on and off, and have some sort of effect.
    This effect is stored in an object variable.
    Please name each switch object after a function, and check self.toggle to see activation.

    Parameters
    ----------
    image_off : str
        The name of the image the switch takes up when it is OFF.
        This must be the exact name of the image as in the file, with the appropriate file extension.        
        For example, if the switch image file is 'switch.png' then this must be this.

    image_on: str
        The name of the image the switch takes up when it is ON.
        *Important* : Make sure that this image has the SAME RESOLUTION as image_off.
        Otherwise, improper collision detection may happen, and you may not get a good blit.
    
    x, y : int
        The x and y coordinate placements for the TOP LEFT of the switch.
        The switch's dimensions are based on the image used.

    toggle : bool, optional (default=False)
        This is the toggle state the switch starts at when it is first spawned.
        The default for this is off, or False. 
    """
    def __init__(self, image_off, image_on, x, y, toggle=False):
        super(Switch, self).__init__()
        self.i_on = image_on
        self.i_off = image_off
        if toggle:
            self.img_main = image_on
        else:
            self.img_main = image_off
        self.image = pygame.image.load(self.img_main)
        self.toggle = toggle  # start by default untoggled
        self.rect = self.image.get_rect()  # get rectangle of image
        self.rect.x, self.rect.y = x, y

    def update(self, event):
        """
        Updates the switch based on the pygame.event event.
        :param event: pygame.event event
            Please put this update function in the main event loop.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # check collision
                self.toggle = not self.toggle  # switch toggle
                if self.toggle:
                    self.img_main = self.i_on  # get correct image
                else:
                    self.img_main = self.i_off
                self.image = pygame.image.load(self.img_main)

    def draw(self, screen):
        """Draw to screen."""
        screen.blit(self.image, self.rect)
