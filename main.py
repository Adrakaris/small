import pygame

from bird import Bird
from constants import FRAMERATE, HEIGHT, PIPE_WIDTH, WIDTH
from pipe import create_pipe

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 


BIRD_STARTING_X = 480
BIRD_STARTING_Y = HEIGHT // 2
GAP_BETWEEN_PIPES = 300

pipe_speed = 4
bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
pipes = []

# =====

def manage_pipes():
    """Generation, moving, and deleting of pipes"""
    # 1. move the pipes
    for pipe in pipes:
        pipe.move(pipe_speed)

    # 2. generate the pipes
    can_generate_new_pipe = len(pipes) == 0 or WIDTH - pipes[-1].x_pos >= GAP_BETWEEN_PIPES + PIPE_WIDTH
    if can_generate_new_pipe:
        new_pipe = create_pipe()
        pipes.append(new_pipe)
    
    # 3. delete unused pipes
    pipes_x = pipes[0].x_pos
    if pipes_x < -PIPE_WIDTH:
        pipes.pop(0)

# =======

done = False 

while not done:
    # game loop
    
    # process player events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    
    # update logic and physics
    bird.update()
    manage_pipes()
    
    # draw stuff!
    screen.fill("white")  # todo: hex codes

    if bird.has_hit_pipe(pipes):
        screen.fill(0xf09b95)
    
    for pipe in pipes:
        pipe.draw(screen)
    bird.draw(screen)
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
