import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, size=3, velocity_range=(-3, 3), gravity=0.2, fade_speed=3, life_span=60):
        self.x = x
        self.y = y
        self.color = color
        self.original_color = color
        self.size = size
        self.original_size = size
        
        # Random velocity
        self.vel_x = random.uniform(velocity_range[0], velocity_range[1])
        self.vel_y = random.uniform(velocity_range[0], velocity_range[1])
        
        # Physics
        self.gravity = gravity
        
        # Lifetime
        self.life = 255  # Alpha value for fading
        self.fade_speed = fade_speed
        self.life_span = life_span
        self.frame_count = 0
        
    def update(self):
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Apply gravity
        self.vel_y += self.gravity
        
        # Decrease life (fade)
        self.life = max(0, self.life - self.fade_speed)
        
        # Shrink particle over time
        if self.frame_count < self.life_span:
            self.size = self.original_size * (1 - (self.frame_count / self.life_span))
        else:
            self.size = 0
            
        self.frame_count += 1
        
    def draw(self, window):
        # Create a fading effect using alpha
        if self.life > 0 and self.size > 0:
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            particle_alpha = min(255, self.life)
            
            # Get the RGB values from the original color
            r, g, b = self.original_color
            
            # Use a circle for the particle
            pygame.draw.circle(
                particle_surface, 
                (r, g, b, particle_alpha), 
                (self.size, self.size), 
                self.size
            )
            
            window.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))
            
    def is_alive(self):
        return self.life > 0 and self.frame_count < self.life_span

class ParticleManager:
    def __init__(self):
        self.particles = []
        
    def add_impact_particles(self, x, y, color=(255, 255, 255), count=20):
        for _ in range(count):
            self.particles.append(
                Particle(
                    x, 
                    y, 
                    color, 
                    size=random.uniform(1, 4),
                    velocity_range=(-4, 4),
                    gravity=0.2,
                    fade_speed=random.uniform(2, 5),
                    life_span=random.randint(30, 60)
                )
            )
    
    def add_feather_particles(self, x, y, count=10):
        feather_colors = [(255, 255, 240), (255, 255, 200), (255, 250, 220)]
        for _ in range(count):
            color = random.choice(feather_colors)
            self.particles.append(
                Particle(
                    x, 
                    y, 
                    color, 
                    size=random.uniform(1, 3),
                    velocity_range=(-3, 3),
                    gravity=0.05,  # Feathers fall slower
                    fade_speed=random.uniform(1, 3),
                    life_span=random.randint(60, 120)
                )
            )
    
    def add_ground_dust(self, x, y, count=15):
        dust_colors = [(139, 69, 19), (160, 82, 45), (210, 180, 140)]
        for _ in range(count):
            # Particles mainly spread horizontally when hitting ground
            vel_x = random.uniform(-5, 5)
            vel_y = random.uniform(-2, 0)  # More upward than downward
            
            particle = Particle(
                x + random.uniform(-10, 10),  # Spread along ground
                y + random.uniform(-2, 2), 
                random.choice(dust_colors), 
                size=random.uniform(1, 3),
                velocity_range=(vel_x, vel_y),
                gravity=0.1,
                fade_speed=random.uniform(3, 6),
                life_span=random.randint(20, 40)
            )
            self.particles.append(particle)
    
    def update(self):
        # Update all particles and remove dead ones
        self.particles = [particle for particle in self.particles if particle.is_alive()]
        
        for particle in self.particles:
            particle.update()
            
    def draw(self, window):
        for particle in self.particles:
            particle.draw(window) 