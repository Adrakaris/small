import pygame

from constants import HEIGHT, PIPE_WIDTH

class PipePair:
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
        
    def draw(self, screen:pygame.Surface):
        top, bottom = self.hitbox()
        pygame.draw.rect(screen, "darkgreen", top)
        pygame.draw.rect(screen, "darkgreen", bottom)

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

