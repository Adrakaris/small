import pygame

from camera import Camera
from constants import FloatRect, Pair

WIDTH = 1200
HEIGHT = 960
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock() 

class Game:
    def __init__(self) -> None:
        self.camera = Camera(Pair(16, 10), Pair.of(screen.get_size()), centre=Pair(8, 5))

    def handle_events(self, events:list[pygame.event.Event]):
        """Process all events in the event queue this cycle"""
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.camera.set_screen_size(screen.get_size())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(f"Mouse pressed at world coordinates {self.camera.world(Pair.of(pygame.mouse.get_pos()))}")

    def update(self, dt:float):
        """Updates game logic"""
        ...

    def draw(self, screen:pygame.SurfaceType):
        """Draws things to the screen. Make sure to convert to screen coordinates"""
        camera = self.camera
        screen.fill("black")

        sr = camera.screen(FloatRect(0, 0, 16, 10))
        pygame.draw.rect(screen, "red", sr, width=3)


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
