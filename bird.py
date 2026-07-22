import math
import pygame

from constants import HEIGHT
from pipe import PipePair
from utils import scale_to_new_size 

HITBOX_RADIUS = 30
GRAVITY = 0.5  # pixels per frame^2
TERMINAL_VELOCITY = 10
JUMP_STRENGTH = -10  # up is negative
JUMP_ACCELERATION = -6  # up is negative
JUMP_ACCELERATION_DECAY = 1/3  # every frame, acceleration is reduced to 1/3 its original value
# first frame -6, second frame -2, then -2/3


class Bird:
    bird_flap_neutral = scale_to_new_size(pygame.image.load("assets/bird-flap-neutral.png"), new_width=int(HITBOX_RADIUS*2.5))
    bird_flap_up = scale_to_new_size(pygame.image.load("assets/bird-flap-up.png"), new_width=int(HITBOX_RADIUS*2.5))
    bird_flap_down = scale_to_new_size(pygame.image.load("assets/bird-flap-down.png"), new_width=int(HITBOX_RADIUS*2.5))
    
    def __init__(self, inital_x:int, initial_y: int) -> None:
        self.centre_x = inital_x
        self.centre_y = initial_y
        self.radius = HITBOX_RADIUS
        self.velocity_y = 0
        self.acceleration_y = 0
        self.dead = False
        self.game_speed = 1
        
    def draw(self, screen:pygame.Surface):
        if abs(self.velocity_y) < 3:
            image_to_draw = self.bird_flap_neutral
        elif self.velocity_y <= -3:
            image_to_draw = self.bird_flap_down
        else:
            image_to_draw = self.bird_flap_up

        image_to_draw = pygame.transform.rotate(image_to_draw, math.degrees(math.atan(-self.velocity_y / self.game_speed / 2)))
        bird_image_destination = image_to_draw.get_rect(center=(self.centre_x, self.centre_y - 5))

        screen.blit(image_to_draw, bird_image_destination)
        
    def update(self, pipes:list[PipePair]):
        hitbox = self.hitbox()
        # since y increases as you go down, we ADD to go down 
        self.centre_y += self.velocity_y
        self.velocity_y += GRAVITY
        self.velocity_y += self.acceleration_y
        self.acceleration_y *= JUMP_ACCELERATION_DECAY
        
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
        self.velocity_y = 0
        self.acceleration_y = JUMP_ACCELERATION

    def set_game_speed(self, new_speed:float):
        self.game_speed = new_speed
        
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

    def has_passed_pipe(self, pipe_list:list[PipePair]) -> bool:
        """Returns true if the bird has passed any of these pipes for the first time"""
        hitbox = self.hitbox()
        for pipe in pipe_list:
            if not pipe.passed and hitbox.x > pipe.x_pos + pipe.width:
                pipe.passed = True
                return True 
        return False
