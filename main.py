import pygame
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.assets import load_assets
from src.game.controller import GameController

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    
    # Load game assets
    assets = load_assets()
    
    # Create and run game controller
    game = GameController(window, assets)
    game.run()
    
if __name__ == "__main__":
    main() 