import pygame
import math
from ..utils.constants import BIRD_WIDTH, BIRD_HEIGHT, WINDOW_HEIGHT, GROUND_HEIGHT, GRAVITY

class Bird:
    def __init__(self, image):
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.gravity = GRAVITY
        self.velocity = 0
        self.tilt = 0
        self.tilt_velocity = 0.5
        self.max_tilt = 25
        self.animation_tick = 0
        self.animation_speed = 5  # Control animation speed
        self.is_dead = False
        self.drop_velocity = 0
        self.image = image
        
        # Death animation properties
        self.death_rotation = 0
        self.death_rotation_speed = 15
        self.death_fall_acceleration = 1.5
        self.hit_ground = False
        self.bounce_count = 0
        self.max_bounces = 2
        self.bounce_height = 10
        self.bounce_decay = 0.6  # Each bounce is smaller
        self.death_shake = 0  # For death shake effect
        self.shake_intensity = 3

    def update(self):
        # Check if bird hits the ground
        ground_y = WINDOW_HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT
        
        if not self.is_dead:
            self.velocity += self.gravity
            self.y += self.velocity

            # Tilt bird based on velocity
            if self.velocity < 0:
                self.tilt = max(self.tilt - self.tilt_velocity, -self.max_tilt)
            else:
                self.tilt = min(self.tilt + self.tilt_velocity, self.max_tilt)

            # Prevent bird from going above the screen
            if self.y < 0:
                self.y = 0
                self.velocity = 0
                
            # Check if bird hits the ground - make sure it dies
            if self.y >= ground_y:
                self.y = ground_y
                self.is_dead = True
                self.hit_ground = True
                self.velocity = 0

            # Animate flapping
            self.animation_tick += 1
            if self.animation_tick >= self.animation_speed:
                self.animation_tick = 0
        else:
            # Handle death animation
            if not self.hit_ground:
                # Accelerate fall when dead
                self.drop_velocity += self.gravity * self.death_fall_acceleration
                self.y += self.drop_velocity
                
                # Rotate bird downward when falling
                if self.death_rotation < 90:
                    self.death_rotation += self.death_rotation_speed
                self.tilt = self.death_rotation
                
                # Add death shake effect (horizontal wobble)
                self.death_shake = math.sin(pygame.time.get_ticks() / 50) * self.shake_intensity
                
                # Check if bird hits the ground
                if self.y >= ground_y:
                    self.y = ground_y
                    self.hit_ground = True
                    self.bounce_count = 0
                    self.drop_velocity = -self.bounce_height  # Initial bounce
            else:
                # Bouncing effect when hitting the ground
                if self.bounce_count < self.max_bounces:
                    self.drop_velocity += self.gravity
                    self.y += self.drop_velocity
                    
                    # If reaching peak of bounce, start falling again
                    if self.drop_velocity >= 0 and self.y >= ground_y:
                        self.y = ground_y
                        self.bounce_count += 1
                        # Each bounce is smaller
                        self.drop_velocity = -self.bounce_height * (self.bounce_decay ** self.bounce_count)
                else:
                    # Final resting position
                    self.y = ground_y
                    self.drop_velocity = 0

    def jump(self):
        if not self.is_dead:
            self.velocity = -12
            self.tilt = -self.max_tilt

    def reset_position(self):
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.tilt = 0
        self.is_dead = False
        self.drop_velocity = 0
        self.death_rotation = 0
        self.hit_ground = False
        self.bounce_count = 0
        self.death_shake = 0

    def draw(self, window):
        # Apply rotation
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        
        # Get position, accounting for death shake if dead
        pos_x = self.x
        if self.is_dead and not self.hit_ground:
            pos_x += self.death_shake
            
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(pos_x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_rect(self):  # Using rectangular hitbox
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)
        
    def is_on_ground(self):
        return self.hit_ground 