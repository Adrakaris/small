
import pygame
import pygame.gfxdraw
from pygame.draw import aaline

from camera import Camera
from constants import BLACK, RED, WHITE, FloatRect, Pair


class Graph:
    def __init__(self, bounds:FloatRect) -> None:
        self.bounds = bounds

        self.points:list[Pair] = []

        self.line_start:Pair|None = None 
        self.line_end:Pair|None = None

    def handle_event(self, event:pygame.event.Event, camera:Camera):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = camera.world(Pair.of(pygame.mouse.get_pos()))
            if self.bounds.collidepoint(pos):
                self.points.append(pos)

    def draw(self, screen:pygame.Surface, camera:Camera):
        # draw axes 
        pygame.draw.line(screen, BLACK, camera.screen(self.bounds.bottomleft), camera.screen(self.bounds.bottomright), width=2)
        pygame.draw.line(screen, BLACK, camera.screen(self.bounds.bottomleft), camera.screen(self.bounds.topleft), width=2)

        if self.line_start is not None and self.line_end is not None:
            x1, y1 = camera.screen(self.line_start).intTuple()
            x2, y2 = camera.screen(self.line_end).intTuple()
            pygame.draw.line(screen, RED, (x1,y1), (x2,y2), width=3)

        for point in self.points:
            x, y = camera.screen(point).intTuple()
            pygame.draw.circle(screen, RED, (x,y) ,5)
            

    def clear_points(self):
        self.points.clear()

    def clear_line(self):
        self.line_start = self.line_end = None

    def get_normalised_points(self) -> list[Pair]:
        """Get all x, y points on the graph, but normalised to 0 to 1 based on the bounds"""
        x, y, w, h = self.bounds.tuple()
        points = [
            Pair((p.x-x)/w, (p.y-y)/h)
            for p in self.points
        ]
        return points

    def set_line(self, y_at_x_0:float, y_at_x_1:float):
        """
        Sets the line on the graph. Provide the y values, normalised between 0 and 1, 
        for the values x=0 and x=1
        """

        self.line_start = Pair(self.bounds.x, self.bounds.y + self.bounds.h*y_at_x_0)
        self.line_end = Pair(self.bounds.x + self.bounds.w, self.bounds.y + self.bounds.h*y_at_x_1)
