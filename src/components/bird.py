import pygame
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

    def update(self):
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

            # Animate flapping
            self.animation_tick += 1
            if self.animation_tick >= self.animation_speed:
                self.animation_tick = 0
        else:
            # Drop animation when dead
            self.drop_velocity += self.gravity
            self.y += self.drop_velocity
            self.tilt = 90  # Rotate bird vertically when falling

            # Check if bird hits the ground
            if self.y + BIRD_HEIGHT >= WINDOW_HEIGHT - GROUND_HEIGHT:
                self.y = WINDOW_HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT
                self.drop_velocity = 0  # Stop dropping once it hits the ground

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

    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_rect(self):  # Using rectangular hitbox
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT) 