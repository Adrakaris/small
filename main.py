import pygame

from bird import Bird
from constants import FRAMERATE, HEIGHT, PIPE_WIDTH, WIDTH
from pipe import PipePair, create_pipe

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

GAME_FONT = pygame.font.SysFont("Hack", 24)
BIRD_STARTING_X = 480
BIRD_STARTING_Y = HEIGHT // 2
GAP_BETWEEN_PIPES = 300

pipe_speed = 4
bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
pipes:list[PipePair] = []
score = 0

# rendering fonts (generating text using fonts) is EXPENSIVE (uses a lot of computing power)
# AVOID doing it every frame if at all possible (reuse existing surface when it doesn't need to be changed)
def update_score_text() -> pygame.Surface:
    return GAME_FONT.render(f"Score: {score}", True, "black")
 
score_text = update_score_text()

# =====

def manage_pipes():
    """Generation, moving, and deleting of pipes"""
    # 1. move the pipes
    for pipe in pipes:
        pipe.move(pipe_speed)

    # 2. generate the pipes
    can_generate_new_pipe = len(pipes) == 0 or WIDTH - pipes[-1].x_pos >= GAP_BETWEEN_PIPES + PIPE_WIDTH
    if can_generate_new_pipe:
        new_pipe = create_pipe()
        pipes.append(new_pipe)
    
    # 3. delete unused pipes
    pipes_x = pipes[0].x_pos
    if pipes_x < -PIPE_WIDTH:
        pipes.pop(0)


def reset_game():
    # Don't use it unless you know what you're doing
    global bird, pipes, score, score_text
    
    bird = Bird(BIRD_STARTING_X, BIRD_STARTING_Y)
    pipes = []
    score = 0
    score_text = update_score_text()

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
                bird.jump()
            if event.key == pygame.K_ESCAPE:
                reset_game()
    
    # update logic and physics
    if not bird.dead:
        bird.update(pipes)
        manage_pipes()

        if bird.has_passed_pipe(pipes):
            score += 1
            score_text = update_score_text()
    
    # draw stuff!
    screen.fill("white")  # todo: hex codes

    if bird.dead:
        screen.fill(0xff7777)
    
    for pipe in pipes:
        pipe.draw(screen)
    bird.draw(screen)

    # gets a rectangle that fits the score text centered at the specified coords
    score_text_hitbox = score_text.get_rect(center=(WIDTH // 2, 48))
    screen.blit(score_text, score_text_hitbox)
    
    pygame.display.flip()
    clock.tick(FRAMERATE)    
    

pygame.quit()
