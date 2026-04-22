import pygame

from bird import Bird
from constants import FRAMERATE, HEIGHT, WIDTH

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 


BIRD_STARTING_X = 480
BIRD_STARTING_Y = HEIGHT // 2

bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)


done = False 

while not done:
    # game loop
    
    # process player events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # update logic and physics
    bird.update()
    
    # draw stuff!
    screen.fill("white")  # todo: hex codes
    
    bird.draw(screen)
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
