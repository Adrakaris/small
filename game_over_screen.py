import pygame

from constants import BIG_GAME_FONT, GAME_FONT, HEIGHT, WIDTH

class GameOverScreen:

    def __init__(self) -> None:
        self.game_over_text = BIG_GAME_FONT.render("GAME OVER", True, "black")
        self.game_over_text_hitbox = self.game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.reset_game_text = GAME_FONT.render("Press [Esc] to restart", True, "black")
        self.reset_game_text_hitbox = self.reset_game_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + self.game_over_text_hitbox.height // 2 + 10)
        )

    def draw(self, screen:pygame.Surface):
        screen.blit(self.game_over_text, self.game_over_text_hitbox)
        screen.blit(self.reset_game_text, self.reset_game_text_hitbox)
