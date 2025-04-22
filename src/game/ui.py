import pygame
from ..components.button import Button
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, SCORE_COLOR, GROUND_COLOR, GROUND_HEIGHT

class UI:
    def __init__(self, window, font):
        self.window = window
        self.font = font
        self.large_font = pygame.font.SysFont(None, 72)  # Larger font for titles
        self.medium_font = pygame.font.SysFont(None, 48)  # Medium font for subtitles
        
        # Create buttons
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
        
        # Game over buttons
        self.restart_button = Button(
            "Restart", 
            WINDOW_WIDTH // 2 - 120, 
            WINDOW_HEIGHT // 2 + 100, 
            100, 
            50, 
            BUTTON_COLOR, 
            BUTTON_HOVER_COLOR,
            font
        )
        
        self.menu_button = Button(
            "Main Menu", 
            WINDOW_WIDTH // 2 + 20, 
            WINDOW_HEIGHT // 2 + 100, 
            100, 
            50, 
            BUTTON_COLOR, 
            BUTTON_HOVER_COLOR,
            font
        )
        
        # Death animation properties
        self.fade_alpha = 0
        self.show_death_screen = False
    
    def draw_main_menu(self, background_image):
        # Draw background
        self.window.blit(background_image, (0, 0))
        
        # Draw title
        title_text = self.large_font.render("Flappy Bird", True, SCORE_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.window.blit(title_text, title_rect)
        
        # Draw start button
        self.start_button.draw(self.window)
    
    def draw_game_over(self, score, is_new_high_score=False, high_score=0):
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(self.fade_alpha, 180)))  # Semi-transparent black
        self.window.blit(overlay, (0, 0))
        
        if not self.show_death_screen:
            return
        
        # Draw "Game Over" text with shadow effect
        game_over_text = self.large_font.render("Game Over", True, (200, 0, 0))  # Red text
        shadow_text = self.large_font.render("Game Over", True, (0, 0, 0))  # Black shadow
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 30))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 3 - 27))  # Offset shadow
        
        self.window.blit(shadow_text, shadow_rect)  # Draw shadow first
        self.window.blit(game_over_text, game_over_rect)  # Draw text on top
        
        # Add a decorative line under "Game Over"
        line_y = game_over_rect.bottom + 10
        pygame.draw.line(
            self.window,
            (150, 0, 0),  # Darker red
            (WINDOW_WIDTH // 2 - 100, line_y),
            (WINDOW_WIDTH // 2 + 100, line_y),
            3
        )
        
        # Draw score with glow effect
        score_text = self.medium_font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.window.blit(score_text, score_rect)
        
        # Draw high score
        if is_new_high_score:
            high_score_text = self.medium_font.render(f"New High Score!", True, (255, 215, 0))  # Gold color
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.window.blit(high_score_text, high_score_rect)
        else:
            high_score_text = self.font.render(f"High Score: {high_score}", True, SCORE_COLOR)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.window.blit(high_score_text, high_score_rect)
        
        # Draw restart button with a small label above
        restart_label = self.font.render("Try Again?", True, SCORE_COLOR)
        restart_label_rect = restart_label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        self.window.blit(restart_label, restart_label_rect)
        
        # Draw buttons
        self.restart_button.draw(self.window)
        self.menu_button.draw(self.window)
    
    def update_death_animation(self, bird_on_ground):
        # If bird hits ground, start fading in the overlay
        if bird_on_ground:
            if self.fade_alpha < 255:
                self.fade_alpha += 5  # Fade in speed
            
            # Show death screen when fade is at 50%
            if self.fade_alpha > 128 and not self.show_death_screen:
                self.show_death_screen = True
    
    def reset_death_animation(self):
        self.fade_alpha = 0
        self.show_death_screen = False
    
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