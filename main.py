import math
from typing import Callable
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
    max_length = 13
    
    def __init__(self) -> None:
        self.box = pygame.Rect(20, 20, 360, 85)
        self.negative_sign = font.render("-", True, BLACK)
        self.negative_sign_box = self.negative_sign.get_rect(center=(45, self.box.centery))
        
        self.buffer = ""
        self.last_number = 0
        self.binary_operation = lambda x, y : x
        
        self.has_decimal = False
        self.negative = False
        self.clear_on_next_input = False 
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (200, 200, 200), self.box)
        
        text = font.render(self.buffer, True, BLACK)
        text_box = text.get_rect(center=self.box.center)
        text_box.x = (self.box.x + self.box.w) - text_box.w - 20
        
        screen.blit(text, text_box)
        if self.negative:
            screen.blit(self.negative_sign, self.negative_sign_box)
            
    def retrieve_number(self):
        if len(self.buffer) == 0:
            return 0.0
        
        num = float(self.buffer)
        if self.negative:
            num = -num 
        return num
        
    def put_number(self, num:float):
        num_str = str(float(num))
        
        split = num_str.split("e")
        decimal = split[0]
        exponent = "e" + split[1][1:] if len(split) > 1 else ""
        
        split = decimal.split(".")
        major_digits = split[0]
        minor_digits = split[1] if len(split) > 1 and split[1] != "0" else ""
        
        if major_digits[0] == "-":
            major_digits = major_digits[1:]
            self.negative = True
               
        if len(major_digits) > self.max_length:
            exponent = f"e{len(major_digits) - 1}"
            first = major_digits[0]
            second = major_digits[1:self.max_length - len(exponent) - 1]
            self.buffer = first + "." + second + exponent
        else:
            first = major_digits[:self.max_length - len(exponent)]
            if minor_digits:
                second = "." + minor_digits[:self.max_length - len(exponent) - len(first) - 1]
            else:
                second = ""
            self.buffer = first + second + exponent

        self.clear_on_next_input = True 
        
    def put_error(self):
        self.buffer = "Error"
        self.negative = False
        self.clear_on_next_input = True
    
    def add_number_character(self, number:str):
        if self.clear_on_next_input:
            self.clear()
        
        if len(self.buffer) >= self.max_length:
            return 
        
        self.buffer += number
        
    def add_decimal(self):
        if self.clear_on_next_input:
            self.clear()
            
        if self.has_decimal or len(self.buffer) >= self.max_length - 1:
            return 
        
        self.buffer += "."
        self.has_decimal = True
        
    def toggle_negative(self):
        if self.clear_on_next_input:
            self.clear()
            
        self.negative = not self.negative
        
    def execute_operation(self, operation:Callable[[float, float], float]):
        self.put_number(operation(self.last_number, self.retrieve_number()))
        self.last_number = 0
        
    def do_square_root(self):
        num = self.retrieve_number()
        
        if num < 0:
            self.put_error()
        else:        
            self.put_number(math.sqrt(self.retrieve_number()))    
            
    def do_add(self):
        self.last_number = self.retrieve_number()
        self.binary_operation = lambda x, y: x + y
        self.clear()
            
    def do_equals(self):
        self.execute_operation(self.binary_operation)
        
    def clear(self):
        self.buffer = ""
        self.has_decimal = False
        self.negative = False 
        self.clear_on_next_input = False
    


calculator = Calcuator()

def mouse_collides_with_box(box:pygame.Rect):
    return box.collidepoint(pygame.mouse.get_pos())

def add_to_calculator(value):
    
    def inner():
        calculator.add_number_character(value)
    
    return inner

def make_green_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, GREEN_BUTTON, GREEN_BUTTON_HOVER, GREEN_BUTTON_PRESSED)

def make_red_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, RED_BUTTON, RED_BUTTON_HOVER, RED_BUTTON_PRESSED)

def make_grey_button(on_clicked, text, x, y, width, height):
    return Button(on_clicked, pygame.Rect(x, y, width, height), text, GREY_BUTTON, GREY_BUTTON_HOVER, GREY_BUTTON_PRESSED)


all_buttons = [
    make_green_button(add_to_calculator("^"), "^", 20, 125, 75, 75),
    make_green_button(calculator.do_square_root, "√", 115, 125, 75, 75),
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
    make_green_button(calculator.do_equals, "=", 210, 505, 75, 75),
    make_green_button(add_to_calculator("+"), "+", 305, 505, 75, 75)
]

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Calculator")
    
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


if __name__ == "__main__":
    main()
