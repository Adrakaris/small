import pygame

pygame.init()

WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

button_box = pygame.Rect(40, 80, 80, 40)
button_colour = (33, 196, 50)  # a green
button_hover_colour = (85, 217, 98)


done = False 
while not done:
    # update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
            
        if event.type == pygame.MOUSEBUTTONUP:
            if button_box.collidepoint(pygame.mouse.get_pos()):
                print("Clicked!")
            
    
    
    # draw
    screen.fill(WHITE)
    
    if button_box.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_hover_colour, button_box)
    else:
        pygame.draw.rect(screen, button_colour, button_box)
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
