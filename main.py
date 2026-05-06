import pygame

from bird import Bird
from constants import FRAMERATE, HEIGHT, PIPE_WIDTH, WIDTH
from pipe import PipePair

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 


BIRD_STARTING_X = 480
BIRD_STARTING_Y = HEIGHT // 2
GAP_BETWEEN_PIPES = 300

pipe_speed = 3
bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
pipes = [PipePair(700, 300, 200)]

# =====

def manage_pipes():
    """Generation, moving, and deleting of pipes"""
    # 1. move the pipes
    for pipe in pipes:
        pipe.move(pipe_speed)

    # 2. generate the pipes
    #       - if there are no pipes, we generate a pipe
    #       - if the pipe gap is big enough we generate a pipe
    #    IF we generate the pipe 100 px to the right of the screen
    #    THEN the gap is big enough when the last pipe in sequence is 200 + PIPE_WIDTH past

    # we need to generate pipes
    # / which means: we need to know when to generate pipes
    # / which means: either: (a) there's no pipes, or (b) the LAST pipe in the list is 
    #   GAP_BETWEEN_PIPES + PIPE_WIDTH position away from WIDTH

    can_generate_new_pipe = len(pipes) == 0 or WIDTH - pipes[-1].x_pos >= GAP_BETWEEN_PIPES + PIPE_WIDTH
    if can_generate_new_pipe:
        ...

    # we know we CAN generate a pipe now. We need to add a pipe to the END of the pipes list
    # which means: we need to know how to create a pipe to add
    # which means: we need to generate the values to create a pipe x_pos:float, gap_y:int, gap_height:int

    # 3. delete unused pipes
    #       - if a pipe is entirely off the screen
    #       - if the first pipe in the list os more than 300px off the left side, o r if there's more than 7 pipes

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
    
    for pipe in pipes:
        pipe.draw(screen)
    bird.draw(screen)
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
