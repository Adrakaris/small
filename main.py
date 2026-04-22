import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720
FRAMERATE = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

done = False 

while not done:
    # game loop
    
    # process player events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # update logic and physics
    
    # draw stuff!
    screen.fill("white")  # todo: hex codes
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
