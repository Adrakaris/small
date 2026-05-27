import pygame

from constants import HEIGHT
from pipe import PipePair 

HITBOX_RADIUS = 30
GRAVITY = 0.5  # pixels per frame^2
TERMINAL_VELOCITY = 10
JUMP_STRENGTH = -10  # up is negative


class Bird:
    
    def __init__(self, inital_x:int, initial_y: int) -> None:
        self.centre_x = inital_x
        self.centre_y = initial_y
        self.radius = HITBOX_RADIUS
        self.velocity_y = 0
        self.dead = False
        
    def draw(self, screen:pygame.Surface):
        pygame.draw.rect(screen, "red", self.hitbox())
        
    def update(self, pipes:list[PipePair]):
        hitbox = self.hitbox()
        
        # since y increases as you go down, we ADD to go down 
        self.centre_y += self.velocity_y
        self.velocity_y += GRAVITY
        
        # preventing the bird from falling too quickly
        if self.velocity_y >= TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY

        # stops the bird if it hits the ceiling
        if hitbox.top <= 0 and self.velocity_y < 0:
            self.velocity_y = 0
            self.centre_y = self.radius
            
        # stops the bird if it hits the floor 
        if hitbox.bottom >= HEIGHT and self.velocity_y > 0:  
            self.dead = True

        if self.has_hit_pipe(pipes):
            self.dead = True
            
    def jump(self):
        self.velocity_y = JUMP_STRENGTH
        
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(
            self.centre_x - self.radius,  # left
            self.centre_y - self.radius,  # right
            2 * self.radius,  # width
            2 * self.radius  # height
        )

    def has_hit_pipe(self, pipe_list:list[PipePair]) -> bool:
        bird_hitbox = self.hitbox()

        for pipe in pipe_list:
            pipe_hitbox = pipe.hitbox()
            hit = bird_hitbox.colliderect(pipe_hitbox[0]) or bird_hitbox.colliderect(pipe_hitbox[1]) 
            if hit:
                return True

        return False
