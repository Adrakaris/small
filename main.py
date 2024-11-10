from numpy import negative
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN_BUTTON = (33, 196, 50)
GREEN_BUTTON_HOVER = (85, 217, 98)
GREEN_BUTTON_PRESSED = (25, 128, 36)
RED_BUTTON = (186, 39, 39)
RED_BUTTON_HOVER = (217, 56, 56)
RED_BUTTON_PRESSED = (158, 38, 46)
GREY_BUTTON = (180, 180, 180)
GREY_BUTTON_HOVER = (200, 200, 200)
GREY_BUTTON_PRESSED = (140, 140, 140)

FPS = 60
clock = pygame.time.Clock()
WIDTH = 400
HEIGHT = 600
font = pygame.font.SysFont("Arial", 50)


class Button:
    def __init__(self, callback, box, display_text, colour, hover_colour, press_colour):
        self.callback = callback
        self.box = box
        self.colour = colour
        self.hover_colour = hover_colour
        self.press_colour = press_colour
        self.text = font.render(display_text, True, BLACK)
        self.text_hitbox = self.text.get_rect(center=self.box.center)
        self.pressed = False
        
    def on_mouse_down(self):
        if not pygame.mouse.get_pressed()[0]:
            return
        if mouse_collides_with_box(self.box):
            self.pressed = True
            
    def on_mouse_up(self):
        if mouse_collides_with_box(self.box) and self.pressed:
            self.callback()
        self.pressed = False 
        
    def draw(self, screen):
        if self.pressed:
            pygame.draw.rect(screen, self.press_colour, self.box)
        elif mouse_collides_with_box(self.box):
            pygame.draw.rect(screen, self.hover_colour, self.box)
        else:
            pygame.draw.rect(screen, self.colour, self.box)
        screen.blit(self.text, self.text_hitbox)


class Calcuator:
    def __init__(self) -> None:
        self.box = pygame.Rect(20, 20, 360, 85)
        self.negative_sign = font.render("-", True, BLACK)
        self.negative_sign_box = self.negative_sign.get_rect(center=(45, self.box.centery))
        
        self.buffer = ""
        self.max_length = 13
        self.has_decimal = False
        self.negative = False
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (200, 200, 200), self.box)
        
        text = font.render(self.buffer, True, BLACK)
        text_box = text.get_rect(center=self.box.center)
        text_box.x = (self.box.x + self.box.w) - text_box.w - 20
        
        screen.blit(text, text_box)
        if self.negative:
            screen.blit(self.negative_sign, self.negative_sign_box)
        
    def add_number(self, number):
        if len(self.buffer) >= self.max_length:
            return 
        
        self.buffer += number
        
    def add_decimal(self):
        if self.has_decimal or len(self.buffer) >= self.max_length - 1:
            return 
        
        self.buffer += "."
        self.has_decimal = True
        
    def toggle_negative(self):
        self.negative = not self.negative
        
    def clear(self):
        self.buffer = ""
        self.has_decimal = False
        self.negative = False 


calculator = Calcuator()

def mouse_collides_with_box(box:pygame.Rect):
    return box.collidepoint(pygame.mouse.get_pos())

def add_to_calculator(value):
    
    def inner():
        calculator.add_number(value)
    
    return inner

def make_green_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, GREEN_BUTTON, GREEN_BUTTON_HOVER, GREEN_BUTTON_PRESSED)

def make_red_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, RED_BUTTON, RED_BUTTON_HOVER, RED_BUTTON_PRESSED)

def make_grey_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, GREY_BUTTON, GREY_BUTTON_HOVER, GREY_BUTTON_PRESSED)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

all_buttons = [
    make_green_button(add_to_calculator("^"), "^", 20, 125, 75, 75),
    make_green_button(add_to_calculator("√"), "√", 115, 125, 75, 75),
    make_green_button(calculator.toggle_negative, "±", 210, 125, 75, 75),
    make_red_button(calculator.clear, "AC", 305, 125, 75, 75),
    make_grey_button(add_to_calculator("7"), "7", 20, 220, 75, 75),
    make_grey_button(add_to_calculator("8"), "8", 115, 220, 75, 75),
    make_grey_button(add_to_calculator("9"), "9", 210, 220, 75, 75),
    make_green_button(add_to_calculator("÷"), "÷", 305, 220, 75, 75),
    make_grey_button(add_to_calculator("4"), "4", 20, 315, 75, 75),
    make_grey_button(add_to_calculator("5"), "5", 115, 315, 75, 75),
    make_grey_button(add_to_calculator("6"), "6", 210, 315, 75, 75),
    make_green_button(add_to_calculator("×"), "×", 305, 315, 75, 75),
    make_grey_button(add_to_calculator("1"), "1", 20, 410, 75, 75),
    make_grey_button(add_to_calculator("2"), "2", 115, 410, 75, 75),
    make_grey_button(add_to_calculator("3"), "3", 210, 410, 75, 75),
    make_green_button(add_to_calculator("-"), "-", 305, 410, 75, 75),
    make_grey_button(add_to_calculator("0"), "0", 20, 505, 75, 75),
    make_grey_button(calculator.add_decimal, ".", 115, 505, 75, 75),
    make_green_button(add_to_calculator("="), "=", 210, 505, 75, 75),
    make_green_button(add_to_calculator("+"), "+", 305, 505, 75, 75)
]



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
    calculator.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
