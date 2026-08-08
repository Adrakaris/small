from typing import NamedTuple, overload

from pygame import Color, Vector2, Rect

# type definitions

ColorLike = tuple[int, int, int] | tuple[int, int, int, int] | int | Color

# data classes

class Pair(NamedTuple):
    x:float
    y:float

    def vec2(self) -> Vector2:
        return Vector2(self.x, self.y)

    def intTuple(self) -> tuple[int,int]:
        return (int(self.x), int(self.y))

    @classmethod
    @overload
    def of(cls, value:Vector2) -> "Pair": ...
    @classmethod
    @overload
    def of(cls, value:tuple[float,float]) -> "Pair": ...

    @classmethod 
    def of(cls, value:Vector2|tuple[float,float]) -> "Pair":
        """Creates a pair from a pair-like object"""
        match value:
            case Vector2():
                return cls(value.x, value.y)
            case tuple():
                return cls(value[0], value[1])

    def __repr__(self) -> str:
        return f"{{{self.x:.3f}, {self.y:.3f}}}"


class FloatRect(NamedTuple):
    """Rectangle used to store floating point coordinates in world coordinates (y-up)"""
    x:float 
    y:float
    w:float
    h:float

    def rect(self) -> Rect:
        """Warning: will round to integral values"""
        return Rect(self.x, self.y, self.w, self.h)

    @property
    def topleft(self) -> tuple[float, float]:
        return (self.x, self.y)

    @property
    def bottomright(self) -> tuple[float, float]:
        return (self.x + self.w, self.y - self.h)

    @classmethod
    def of(cls, value:Rect) -> "FloatRect":
        return cls(value.x, value.y, value.w, value.h)
    

# COLOURS

BACKGROUND = (214, 211, 208)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (217, 30, 30)
GREEN = (76, 191, 63)
BLUE = (38, 78, 209)

def lighten(colour:ColorLike, factor:float) -> Color:
    """Blend the colour with white. Factor between 0 and 1."""
    _colour = Color(colour)
    return _colour.lerp(WHITE, factor)

def darken(colour:ColorLike, factor:float) -> Color:
    """Blend the colour with black. Factor between 0 and 1."""
    _colour = Color(colour)
    return _colour.lerp(BLACK, factor)
