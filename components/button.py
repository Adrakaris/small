
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from pygame import Color

from constants import ColorTuple

class ButtonType(Enum):
    PRESS = 0
    TOGGLE = 1

@dataclass
class Button:
    """
    Toggle or switch button in pygame, renders as a rectangle with an optional label
    """
    on_colour: Color|ColorTuple|int
    off_colour: Color|ColorTuple|int
    hover_colour: Color|ColorTuple|int
    action: Callable|None
    active = False
    kind = ButtonType.PRESS
