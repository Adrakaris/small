import pygame
from pygame import Rect

from camera import Camera
from components.button import Button
from constants import BACKGROUND, BLACK, GREEN, RED, FloatRect, Pair
from graph import Graph
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

        run_button = Button( FloatRect(16.25, 8, 3.5, 1.5), GREEN, RED,  self.draw_line )
        run_button_label = Text(self.font, "Draw Line", BLACK, Pair(16.5, 9))

        clear_button = Button( FloatRect(16.25, 6.25, 3.5, 1.5), GREEN, RED, self.clear )
        clear_button_label = Text(self.font, "Clear", BLACK, Pair(16.5, 7.25))

        self.buttons = [run_button, clear_button]
        self.labels = [run_button_label, clear_button_label]

        self.graph = Graph(FloatRect(0.25, 0.25, 15.5, 9.5))


    def handle_events(self, events:list[pygame.event.Event]):
        """Process all events in the event queue this cycle"""
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.camera.set_screen_size(screen.get_size())
                self.font.refresh(self.camera)
                for label in self.labels:
                    label.refresh()
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     print(f"Mouse pressed at screen {pygame.mouse.get_pos()} world {self.camera.world(Pair.of(pygame.mouse.get_pos()))}")

            for button in self.buttons:
                button.handle_event(event, self.camera)

            self.graph.handle_event(event, self.camera)

    def update(self, dt:float):
        """Updates game logic"""
        for button in self.buttons:
            button.update(self.camera)

    def draw(self, screen:pygame.SurfaceType):
        """Draws things to the screen. Make sure to convert to screen coordinates"""
        camera = self.camera
        screen.fill(BACKGROUND)

        for button in self.buttons:
            button.draw(screen, camera)
        for label in self.labels:
            label.draw(screen, camera)

        self.graph.draw(screen, camera)

    def draw_line(self):
        print(self.graph.get_normalised_points())
        self.graph.clear_line()
        self.graph.set_line(0.25, 0.75)

    def clear(self):
        self.graph.clear_points()
        self.graph.clear_line()


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
