import random
import pygame

from constants import HEIGHT, PIPE_WIDTH, WIDTH
from utils import scale_to_new_size

class PipePair:
    pipe_top = scale_to_new_size(pygame.image.load("assets/pipe-downwards.png"), new_width=PIPE_WIDTH)
    pipe_bottom = scale_to_new_size(pygame.image.load("assets/pipe-upwards.png"), new_width=PIPE_WIDTH)
    
    """
    A pair of pipes that the bird should pass through
    
    gap_y is the top of the gap, gap_height is the size of the gap, the rest 
    of the column are all pipes
    """
    def __init__(self, x_pos:float, gap_y:int, gap_height:int):
        self.x_pos = x_pos
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.width = PIPE_WIDTH
        self.passed = False
        
    def draw(self, screen:pygame.Surface):
        top, bottom = self.hitbox()

        pipe_top_destination = self.pipe_top.get_rect(bottomleft=top.bottomleft)
        screen.blit(self.pipe_top, pipe_top_destination)
        pipe_bottom_destination = self.pipe_bottom.get_rect(topleft=bottom.topleft)
        screen.blit(self.pipe_bottom, pipe_bottom_destination)

    def move(self, speed:float):
        self.x_pos -= speed

    def hitbox(self) -> tuple[pygame.Rect, pygame.Rect]:
        """Returns two hitboxes: the top pipe, and the bottom pipe"""
        
        top_pipe = pygame.Rect(
            self.x_pos, 
            0,
            self.width, 
            self.gap_y
        )

        bottom_pipe = pygame.Rect(
            self.x_pos,
            self.gap_y + self.gap_height,
            self.width,
            HEIGHT
        )
        
        return (top_pipe, bottom_pipe)



highest_gap_y = 80
lowest_gap_y = 380
possible_gap_widths = [300, 230, 270]

def create_pipe() -> PipePair:
    """randomly generate a pipe configuration"""
    return PipePair(
        WIDTH,  # pipe starts off the right edge of the screen
        random.randint(highest_gap_y, lowest_gap_y),  # top of the gap
        random.choice(possible_gap_widths)
    )
