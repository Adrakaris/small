from typing import NamedTuple, overload

from pygame import Vector2

class Pair(NamedTuple):
    x:float
    y:float

    def vec2(self) -> Vector2:
        return Vector2(self.x, self.y)

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
