import pygame
import os
from .constants import BIRD_WIDTH, BIRD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT

def load_assets():
    """Load and prepare all game assets"""
    assets = {}
    
    # Get the absolute path to the assets directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    
    # Load bird image
    bird_path = os.path.join(assets_dir, "bird.png")
    bird_image = pygame.image.load(bird_path)
    bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
    assets["bird"] = bird_image
    
    # Load background image
    bg_path = os.path.join(assets_dir, "background.png")
    bg_image = pygame.image.load(bg_path)
    bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    assets["background"] = bg_image
    
    return assets 