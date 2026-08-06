from dataclasses import dataclass
from typing import overload 

from pygame import Rect, Vector2

from constants import Pair

@dataclass
class Camera:
    """
    A world camera. **IMPORTANT**: the coordinates here are y-up, not y-down!
    """
    size: Pair
    screen_size: Pair
    centre: Pair = Pair(0, 0)

    def set_screen_size(self, new_size:tuple[int, int]):
        self.screen_size = Pair.of(new_size)

    @overload
    def screen(self, unit:Pair) -> Pair: ...
    @overload
    def screen(self, unit:Vector2) -> Vector2: ...
    @overload
    def screen(self, unit:Rect) -> Rect: ...
    @overload
    def screen(self, unit:float) -> float: ...

    def screen(self, unit:Pair|Rect|Vector2|float):
        """
        Converts world coordinates to screen coordinates, 
        scaled to the size of the screen, maintaining aspect
        ratio.
        """
        scale = min(self.screen_size.x / self.size.x, self.screen_size.y / self.size.y)
        match unit:
            case float() | int():
                return unit * scale 
            case Pair():
                x = (self.screen_size.x / 2) + (unit.x - self.centre.x) * scale
                y = (self.screen_size.y / 2) - (unit.y - self.centre.y) * scale
                return Pair(x, y)
            case Vector2():
                x = (self.screen_size.x / 2) + (unit.x - self.centre.x) * scale
                y = (self.screen_size.y / 2) - (unit.y - self.centre.y) * scale
                return Vector2(x, y)
            case Rect():
                topleft = self.screen(Pair.of(unit.topleft))
                bottomright = self.screen(Pair.of(unit.bottomright))
                x = min(topleft.x, bottomright.x)
                y = min(topleft.y, bottomright.y)
                w = abs(topleft.x - bottomright.x)
                h = abs(topleft.y - bottomright.y)
                return Rect(x, y, w, h)

    @overload
    def world(self, unit:Pair) -> Pair: ...
    @overload
    def world(self, unit:Vector2) -> Vector2: ...
    @overload
    def world(self, unit:Rect) -> Rect: ...
    @overload
    def world(self, unit:float) -> float: ...
    
    def world(self, unit:Pair|Rect|Vector2|float):
        """
        Converts screen coordinates to world coordinates,
        scaled to the size of the world, maintaining aspect
        ratio.
        """
        scale = min(self.screen_size.x / self.size.x, self.screen_size.y / self.size.y)
        match unit:
            case float() | int():
                return unit / scale
            case Pair():
                x = self.centre.x + (unit.x - self.screen_size.x / 2) / scale
                y = self.centre.y - (unit.y - self.screen_size.y / 2) / scale
                return Pair(x, y)
            case Vector2():
                x = self.centre.x + (unit.x - self.screen_size.x / 2) / scale
                y = self.centre.y - (unit.y - self.screen_size.y / 2) / scale
                return Vector2(x, y)
            case Rect():
                topleft = self.world(Pair.of(unit.topleft))
                bottomright = self.world(Pair.of(unit.bottomright))
                x = min(topleft.x, bottomright.x)
                y = min(topleft.y, bottomright.y)
                w = abs(topleft.x - bottomright.x)
                h = abs(topleft.y - bottomright.y)
                return Rect(x, y, w, h)
