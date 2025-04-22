import pygame
from ..components.button import Button
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, SCORE_COLOR, GROUND_COLOR, GROUND_HEIGHT

class UI:
    def __init__(self, window, font):
        self.window = window
        self.font = font
        self.start_button = Button(
            "Start", 
            WINDOW_WIDTH // 2 - 50, 
            WINDOW_HEIGHT // 2 - 25, 
            100, 
            50, 
            BUTTON_COLOR, 
            BUTTON_HOVER_COLOR,
            font
        )
    
    def draw_main_menu(self, background_image):
        # Draw background
        self.window.blit(background_image, (0, 0))
        
        # Draw start button
        self.start_button.draw(self.window)
        
        # Draw title
        title_text = self.font.render("Flappy Bird", True, SCORE_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.window.blit(title_text, title_rect)
    
    def draw_game_over(self, score, is_new_high_score=False, high_score=0):
        # Draw "Game Over" text
        game_over_text = self.font.render("Game Over", True, SCORE_COLOR)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.window.blit(game_over_text, game_over_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.window.blit(score_text, score_rect)
        
        # Draw high score if it's a new high score
        if is_new_high_score:
            high_score_text = self.font.render(f"New High Score: {score}", True, SCORE_COLOR)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.window.blit(high_score_text, high_score_rect)
        
        # Draw restart instructions
        restart_text = self.font.render("Press 'R' to restart", True, SCORE_COLOR)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.window.blit(restart_text, restart_rect)
    
    def draw_score(self, score, high_score):
        # Draw current score
        score_text = self.font.render(f"Score: {score}", True, SCORE_COLOR)
        self.window.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font.render(f"High Score: {high_score}", True, SCORE_COLOR)
        self.window.blit(high_score_text, (10, 50))
    
    def draw_ground(self):
        pygame.draw.rect(
            self.window, 
            GROUND_COLOR, 
            (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT)
        ) 