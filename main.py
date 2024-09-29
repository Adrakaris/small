import pygame

pygame.init()

WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

done = False 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
            
    # update
    
    
    # draw
    screen.fill(WHITE)
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
