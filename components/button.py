
from typing import Any, Callable

from pygame import Color, Rect, SurfaceType
import pygame
from pygame.event import Event

from camera import Camera
from constants import ColorLike, FloatRect, lighten


class Button:
    """
    Toggle button in pygame, renders as a rectangle with an optional label.

    Give rect in world coordinates.
    """
    def __init__(self, rect:FloatRect, on_colour:Color|ColorLike, off_colour:Color|ColorLike, action:Callable[[], Any]) -> None:
        self.rect = rect
        self.on_colour = on_colour
        self.off_colour = off_colour
        self.action = action

        self.pressed = False 
        self.colour = off_colour

    def handle_event(self, event:Event, camera:Camera):
        screen_rect = camera.screen(self.rect)
        if event.type == pygame.MOUSEBUTTONDOWN and screen_rect.collidepoint(pygame.mouse.get_pos()):
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if screen_rect.collidepoint(pygame.mouse.get_pos()):
                self.action()
            self.pressed = False

    def update(self, camera:Camera):
        hovered = camera.screen(self.rect).collidepoint(pygame.mouse.get_pos())
        if not self.pressed:
            if hovered:
                self.colour = lighten(self.off_colour, 0.2)
            else:
                self.colour = self.off_colour
        else:
            self.colour = self.on_colour

    def draw(self, screen:SurfaceType, camera:Camera):
        pygame.draw.rect(screen, self.colour, camera.screen(self.rect))
