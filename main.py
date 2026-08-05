import pygame

WIDTH = 1200
HEIGHT = 960
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

class Game:
    def __init__(self) -> None:
        ...

    def handle_events(self, events:list[pygame.event.Event]):
        ...

    def update(self):
        ...

    def draw(self, screen:pygame.SurfaceType):
        screen.fill("black")


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

    game.update()
    
    game.draw(screen)

    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
    

pygame.quit()
