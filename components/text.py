

from dataclasses import dataclass

import pygame
from pygame.font import Font

from camera import Camera
from constants import ColorLike, Pair

@dataclass
class DynamicFont:
    """Dynamic font object that works with resize. Call refresh() immediately after instantiation"""
    font_name:str
    world_size:float

    def refresh(self, camera:Camera):
        """Re-creates the internal font object after resize"""
        self.font_object = pygame.font.Font(self.font_name, round(camera.screen(self.world_size)))

    def render(self, text:str, colour:ColorLike) -> pygame.Surface:
        return self.font_object.render(text, True, colour)


class Text:
    """Dynamic redrawable text that works with resize"""
    def __init__(self, dynamic_font:DynamicFont, text:str, colour:ColorLike, position:Pair) -> None:
        self.dynamic_font = dynamic_font
        self.text = text
        self.colour = colour
        self.position = position

        self._rendered_text = self.dynamic_font.render(self.text, self.colour)

    def refresh(self):
        """To re-draw the text after the font has been refreshed"""
        self._rendered_text = self.dynamic_font.render(self.text, self.colour)

    def draw(self, screen:pygame.Surface, camera:Camera):
        rect = self._rendered_text.get_rect()
        screen.blit(self._rendered_text, camera.screen(self.position), rect)
