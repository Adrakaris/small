import pygame

from constants import FRAMERATE, HEIGHT, PIPE_WIDTH, WIDTH, GAME_FONT
from bird import Bird
from pipe import PipePair, create_pipe
from game_over_screen import GameOverScreen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

BIRD_STARTING_X = 480
BIRD_STARTING_Y = HEIGHT // 2
GAP_BETWEEN_PIPES = 300

class GameState:
    def __init__(self) -> None:
        self.pipe_speed = 4
        self.bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
        self.pipes:list[PipePair] = []
        
        self.score = 0
        self.score_text = pygame.Surface((0, 0))
        self.high_score = 0
        self.high_score_text = pygame.Surface((0, 0))

        self.set_high_score(0)
        self.set_score(0)

    def set_score(self, new_score:int):
        self.score = new_score
        self.score_text = GAME_FONT.render(f"Score: {self.score}", True, "black") 

    def set_high_score(self, new_high_score:int):
        self.high_score = new_high_score
        self.high_score_text = GAME_FONT.render(f"High: {self.high_score}", True, "grey")

    def reset(self):
        if self.score > self.high_score:
            self.set_high_score(self.score)
        
        self.bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
        self.pipes.clear()
        self.set_score(0)

    def is_dead(self) -> bool:
        return self.bird.dead

    def update_bird(self):
        self.bird.update(self.pipes)

        if self.bird.has_passed_pipe(self.pipes):
            self.set_score(self.score + 1)

        self.update_pipe_speed()

    def update_pipe_speed(self):
        """Every 20 points, increase pipe speed by 0.5"""
        self.pipe_speed = 4 + 0.5 * (self.score // 20)

    def manage_pipes(self):
        """Generation, moving, and deleting of pipes"""
        # 1. move the pipes
        for pipe in self.pipes:
            pipe.move(self.pipe_speed)
    
        # 2. generate the pipes
        can_generate_new_pipe = len(self.pipes) == 0 or WIDTH - self.pipes[-1].x_pos >= GAP_BETWEEN_PIPES + PIPE_WIDTH
        if can_generate_new_pipe:
            new_pipe = create_pipe()
            self.pipes.append(new_pipe)
        
        # 3. delete unused pipes
        pipes_x = self.pipes[0].x_pos
        if pipes_x < -PIPE_WIDTH:
            self.pipes.pop(0)

    
    

game = GameState()
game_over_screen = GameOverScreen()

# =======

done = False 

while not done:
    # game loop
    
    # process player events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.bird.jump()
            if event.key == pygame.K_ESCAPE:
                game.reset()
    
    # update logic and physics
    if not game.is_dead():
        game.update_bird()
        game.manage_pipes()
    
    # draw stuff!
    screen.fill("white")  # todo: hex codes

    if game.is_dead():
        screen.fill(0xff7777)
    
    for pipe in game.pipes:
        pipe.draw(screen)
    game.bird.draw(screen)

    # gets a rectangle that fits the score text centered at the specified coords
    score_text_hitbox = game.score_text.get_rect(center=(WIDTH // 2, 48))
    screen.blit(game.score_text, score_text_hitbox)
    highscore_text_hitbox = game.high_score_text.get_rect(topright=(WIDTH - 36, 36))
    screen.blit(game.high_score_text, highscore_text_hitbox)

    if game.is_dead():
        game_over_screen.draw(screen)
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
