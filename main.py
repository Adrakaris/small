import pygame
from pygame import Rect

from camera import Camera
from components.button import Button
from constants import BACKGROUND, BLACK, GREEN, RED, FloatRect, Pair
from text import DynamicFont, Text

FPS = 60
# width and height of camera in world coordinates
WIDTH, HEIGHT = 20, 10

pygame.init()
screen = pygame.display.set_mode((1500, 750), pygame.RESIZABLE)
clock = pygame.time.Clock() 

class Game:
    def __init__(self) -> None:
        self.camera = Camera(Pair(WIDTH, HEIGHT), Pair.of(screen.get_size()), centre=Pair(10, 5))
        self.font = DynamicFont("assets/hack.ttf", 0.5)
        self.font.refresh(self.camera)

        run_button = Button( FloatRect(16.25, 9.5, 3.5, 1.5), GREEN, RED,  self.boop )
        run_button_label = Text(self.font, "Draw Line", BLACK, Pair(16.5, 9))

        clear_button = Button( FloatRect(16.25, 7.75, 3.5, 1.5), GREEN, RED, self.boop )
        clear_button_label = Text(self.font, "Clear", BLACK, Pair(16.5, 7.25))

        self.buttons = [run_button, clear_button]
        self.labels = [run_button_label, clear_button_label]


    def handle_events(self, events:list[pygame.event.Event]):
        """Process all events in the event queue this cycle"""
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.camera.set_screen_size(screen.get_size())
                self.font.refresh(self.camera)
                for label in self.labels:
                    label.refresh()
                
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     print(f"Mouse pressed at world coordinates {self.camera.world(Pair.of(pygame.mouse.get_pos()))}")

            for button in self.buttons:
                button.handle_event(event, self.camera)

    def update(self, dt:float):
        """Updates game logic"""
        for button in self.buttons:
            button.update(self.camera)

    def draw(self, screen:pygame.SurfaceType):
        """Draws things to the screen. Make sure to convert to screen coordinates"""
        camera = self.camera
        screen.fill(BACKGROUND)

        sr = camera.screen(FloatRect(0, 10, 16, 10))
        pygame.draw.rect(screen, "red", sr, width=3)

        for button in self.buttons:
            button.draw(screen, camera)
        for label in self.labels:
            label.draw(screen, camera)

    def boop(self):
        print("boop!")


game = Game()

# =======

done = False 

while not done:
    dt = 1/FPS
    
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            done = True 
    game.handle_events(events)

    game.update(dt)
    
    game.draw(screen)

    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
    

pygame.quit()
