import pygame
import random
from ..components.bird import Bird
from ..components.pipe import Pipe
from ..components.particle import ParticleManager
from .state import GameState
from .score import ScoreManager
from .ui import UI
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_GAP, GROUND_HEIGHT, FPS, PIPE_SPAWN_TIME, PIPE_WIDTH, PIPE_COLOR, BIRD_WIDTH, BIRD_HEIGHT

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
        self.particle_manager = ParticleManager()
        
        # Set up background scrolling
        self.background_x = 0
        
        # Set up pipe spawning timer
        self.add_pipe_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe_event, PIPE_SPAWN_TIME)
        
        # Death sequence flags
        self.death_time = 0
        self.death_delay = 1000  # milliseconds to wait after bird hits ground
        self.collision_point = None
        self.has_added_death_particles = False
        self.has_added_ground_particles = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_state.is_game_started and not self.game_state.is_game_over:
                        self.game_state.start_game()
                    self.bird.jump()
                
                if event.key == pygame.K_r and self.game_state.is_game_over and self.ui.show_death_screen:
                    self.reset_game()
                    return True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle main menu button click
                if not self.game_state.is_game_started and not self.game_state.is_game_over:
                    if self.ui.start_button.is_clicked():
                        self.game_state.start_game()
                
                # Handle game over screen buttons
                if self.game_state.is_game_over and self.ui.show_death_screen:
                    if self.ui.restart_button.is_clicked():
                        self.reset_game()
                        return True
                    if self.ui.menu_button.is_clicked():
                        self.reset_game()
                        self.game_state.reset()  # Make sure we go to main menu
                        return True
            
            if event.type == self.add_pipe_event and self.game_state.is_game_started and not self.game_state.is_game_over:
                self.spawn_pipe()
        
        return True
    
    def update(self):
        # Always update particles
        self.particle_manager.update()
        
        # Update bird position if game started
        if self.game_state.is_game_started:
            self.bird.update()
            
            # If the bird died from hitting the ground in the update, set game over
            if self.bird.is_dead and not self.game_state.is_game_over:
                self.game_state.end_game()
        
        # Update pipes and check for passing only if game is not over
        if not self.game_state.is_game_over:
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
                    
                    # Check collision with upper pipe
                    if bird_rect.colliderect(upper_pipe_rect):
                        self.game_state.end_game()
                        self.bird.is_dead = True
                        
                        # Find collision point
                        self.collision_point = (
                            max(bird_rect.left, upper_pipe_rect.left),
                            max(bird_rect.top, upper_pipe_rect.top)
                        )
                        
                        # Add impact particles when bird hits
                        if not self.has_added_death_particles:
                            self.particle_manager.add_impact_particles(
                                self.collision_point[0], 
                                self.collision_point[1],
                                PIPE_COLOR,
                                30
                            )
                            self.particle_manager.add_feather_particles(
                                self.bird.x + BIRD_WIDTH//2, 
                                self.bird.y + BIRD_HEIGHT//2,
                                15
                            )
                            self.has_added_death_particles = True
                    
                    # Check collision with lower pipe
                    elif bird_rect.colliderect(lower_pipe_rect):
                        self.game_state.end_game()
                        self.bird.is_dead = True
                        
                        # Find collision point
                        self.collision_point = (
                            max(bird_rect.left, lower_pipe_rect.left),
                            min(bird_rect.bottom, lower_pipe_rect.bottom)
                        )
                        
                        # Add impact particles when bird hits
                        if not self.has_added_death_particles:
                            self.particle_manager.add_impact_particles(
                                self.collision_point[0], 
                                self.collision_point[1],
                                PIPE_COLOR,
                                30
                            )
                            self.particle_manager.add_feather_particles(
                                self.bird.x + BIRD_WIDTH//2, 
                                self.bird.y + BIRD_HEIGHT//2,
                                15
                            )
                            self.has_added_death_particles = True
        
        # Check if bird hits the ground or is already on ground
        if self.bird.is_on_ground():
            if not self.has_added_ground_particles:
                # Add dust particles when the bird hits the ground
                self.particle_manager.add_ground_dust(
                    self.bird.x + BIRD_WIDTH//2,
                    WINDOW_HEIGHT - GROUND_HEIGHT,
                    25
                )
                self.has_added_ground_particles = True
            
            if self.game_state.is_bird_falling:
                self.game_state.bird_hit_ground()
                self.death_time = pygame.time.get_ticks()
            
            # If bird has been on the ground for enough time, update the UI
            if pygame.time.get_ticks() - self.death_time > self.death_delay:
                self.ui.update_death_animation(True)
        
        # Update death animation if bird is dead
        if self.game_state.is_game_over:
            self.score_manager.save_high_score()
        
        # Update background position only if the game is not over
        if not self.game_state.is_game_over:
            self.background_x -= 1  # Move the background by 1 pixel to the left
            if self.background_x <= -WINDOW_WIDTH:
                self.background_x = 0
    
    def render(self):
        # Draw background with scrolling effect
        self.window.blit(self.assets["background"], (self.background_x, 0))
        self.window.blit(self.assets["background"], (self.background_x + WINDOW_WIDTH, 0))
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.window)
        
        # Draw particles
        self.particle_manager.draw(self.window)
        
        # Draw bird only when the game has started
        if self.game_state.is_game_started:
            self.bird.draw(self.window)
        
        # Draw ground
        self.ui.draw_ground()
        
        # Draw score if game is started
        if self.game_state.is_game_started and not self.ui.show_death_screen:
            self.ui.draw_score(self.score_manager.score, self.score_manager.high_score)
        
        # Show main menu screen
        if not self.game_state.is_game_started and not self.game_state.is_game_over:
            self.ui.draw_main_menu(self.assets["background"])
        
        # Show game over screen only after bird has fallen to the ground
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
        self.game_state.start_game()  # Automatically start a new game
        self.score_manager.reset()
        self.bird.reset_position()
        self.pipes.clear()
        self.ui.reset_death_animation()
        self.death_time = 0
        self.collision_point = None
        self.has_added_death_particles = False
        self.has_added_ground_particles = False
        self.particle_manager = ParticleManager()  # Reset particles
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
        
        pygame.quit() 