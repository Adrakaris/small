import pygame


class Button:
    def __init__(self, box, colour, hover_colour, press_colour):
        self.box = box
        self.colour = colour
        self.hover_colour = hover_colour
        self.press_colour = press_colour
        self.pressed = False
        
    def on_mouse_down(self):
        if mouse_collides_with_box(self.box):
            self.pressed = True
            
    def on_mouse_up(self):
        if mouse_collides_with_box(self.box) and self.pressed:
            print("Clicked!")
        self.pressed = False 
        
    def draw(self, screen):
        if self.pressed:
            pygame.draw.rect(screen, self.press_colour, self.box)
        elif mouse_collides_with_box(self.box):
            pygame.draw.rect(screen, self.hover_colour, self.box)
        else:
            pygame.draw.rect(screen, self.colour, self.box)


def mouse_collides_with_box(box:pygame.Rect):
    return box.collidepoint(pygame.mouse.get_pos())


pygame.init()

WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

button_1 = Button(
    pygame.Rect(40, 80, 80, 40), 
    (33, 196, 50), 
    (85, 217, 98), 
    (25, 128, 36)
)

button_2 = Button(
    pygame.Rect(140, 80, 80, 40),
    (186, 39, 39),
    (217, 56, 56),
    (158, 38, 46)
)

all_buttons = [button_1, button_2]

done = False 
while not done:
    # update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in all_buttons:
                button.on_mouse_down()
            
        if event.type == pygame.MOUSEBUTTONUP:
            for button in all_buttons:
                button.on_mouse_up()
    
    # draw
    screen.fill(WHITE)
    
    for button in all_buttons:
        button.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
