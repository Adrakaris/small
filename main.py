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
button_pressed_colour = (25, 128, 36)
button_pressed = False

button_box2 = pygame.Rect(140, 80, 80, 40)
button_colour2 = (186, 39, 39)
button_hover2_colour = (217, 56, 56)
button_pressed2_colour = (158, 38, 46)
button_pressed2 = False 

def mouse_collides_with_box(box:pygame.Rect):
    return box.collidepoint(pygame.mouse.get_pos())

def draw_button(is_button_pressed, 
                button_box, 
                button_colour, 
                button_hover_colour, 
                button_pressed_colour,
                screen):
    if is_button_pressed:
        pygame.draw.rect(screen, button_pressed_colour, button_box)
    elif mouse_collides_with_box(button_box):
        pygame.draw.rect(screen, button_hover_colour, button_box)
    else:
        pygame.draw.rect(screen, button_colour, button_box)

done = False 
while not done:
    # update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_collides_with_box(button_box):
                button_pressed = True
            
            if mouse_collides_with_box(button_box2):
                button_pressed2 = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False 
            if mouse_collides_with_box(button_box):
                print("Clicked!")
            
            button_pressed2 = False
            if mouse_collides_with_box(button_box2):
                print("Clicked 2!")
    
    # draw
    screen.fill(WHITE)
    
    draw_button(button_pressed, button_box, button_colour, button_hover_colour, button_pressed_colour, screen)
    draw_button(button_pressed2, button_box2, button_colour2, button_hover2_colour, button_pressed2_colour, screen)
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
