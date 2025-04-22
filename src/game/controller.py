import pygame
import random
from ..components.bird import Bird
from ..components.pipe import Pipe
from .state import GameState
from .score import ScoreManager
from .ui import UI
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_GAP, GROUND_HEIGHT, FPS, PIPE_SPAWN_TIME, PIPE_WIDTH

class GameController:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.bird = Bird(assets["bird"])
        self.pipes = []
        
        # Create managers
        self.score_manager = ScoreManager()
        self.game_state = GameState()
        self.font = pygame.font.SysFont(None, 36)  # Use a system font
        self.ui = UI(window, self.font)
        
        # Set up background scrolling
        self.background_x = 0
        
        # Set up pipe spawning timer
        self.add_pipe_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe_event, PIPE_SPAWN_TIME)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_state.is_game_started and not self.game_state.is_game_over:
                        self.game_state.start_game()
                    self.bird.jump()
                
                if event.key == pygame.K_r and self.game_state.is_game_over:
                    self.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_state.is_game_started and not self.game_state.is_game_over:
                    if self.ui.start_button.is_clicked():
                        self.game_state.start_game()
            
            if event.type == self.add_pipe_event and self.game_state.is_game_started and not self.game_state.is_game_over:
                self.spawn_pipe()
        
        return True
    
    def update(self):
        # Update bird position if game started
        if self.game_state.is_game_started:
            self.bird.update()
        
        # Update pipes and check for passing
        for pipe in self.pipes:
            pipe.update()
            
            # Remove pipes that are off screen
            if pipe.x + PIPE_WIDTH < 0:
                self.pipes.remove(pipe)
            
            # Check if bird passed the pipe
            if pipe.x + PIPE_WIDTH < self.bird.x:
                if not pipe.passed:
                    pipe.passed = True
                    self.score_manager.increment()
            
            # Check collision
            if self.game_state.is_game_started and not self.game_state.is_game_over:
                bird_rect = self.bird.get_rect()
                upper_pipe_rect, lower_pipe_rect = pipe.get_rect()
                
                if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
                    self.game_state.end_game()
                    self.bird.is_dead = True
        
        # Check if bird hits the ground
        if self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT - GROUND_HEIGHT:
            self.game_state.end_game()
            self.bird.is_dead = True
        
        # Save high score if game is over
        if self.game_state.is_game_over:
            self.score_manager.save_high_score()
        
        # Update background position
        self.background_x -= 1  # Move the background by 1 pixel to the left
        if self.background_x <= -WINDOW_WIDTH:
            self.background_x = 0
    
    def render(self):
        # Draw background with scrolling effect
        self.window.blit(self.assets["background"], (self.background_x, 0))
        self.window.blit(self.assets["background"], (self.background_x + WINDOW_WIDTH, 0))
        
        # Draw ground
        self.ui.draw_ground()
        
        # Draw bird only when the game has started
        if self.game_state.is_game_started:
            self.bird.draw(self.window)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.window)
        
        # Draw score if game is started
        if self.game_state.is_game_started:
            self.ui.draw_score(self.score_manager.score, self.score_manager.high_score)
        
        # Show main menu screen
        if not self.game_state.is_game_started and not self.game_state.is_game_over:
            self.ui.draw_main_menu(self.assets["background"])
        
        # Show game over screen
        if self.game_state.is_game_over:
            self.ui.draw_game_over(
                self.score_manager.score, 
                self.score_manager.is_new_high_score(),
                self.score_manager.high_score
            )
        
        # Update the display
        pygame.display.update()
        self.clock.tick(FPS)
    
    def spawn_pipe(self):
        gap_height = random.randint(50, WINDOW_HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)
        new_pipe = Pipe(WINDOW_WIDTH, gap_height)
        self.pipes.append(new_pipe)
    
    def reset_game(self):
        self.game_state.reset()
        self.score_manager.reset()
        self.bird.reset_position()
        self.pipes.clear()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
        
        pygame.quit() 