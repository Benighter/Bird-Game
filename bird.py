import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 740

# Bird dimensions
BIRD_WIDTH = 50
BIRD_HEIGHT = 40

# Pipe dimensions
PIPE_WIDTH = 80
PIPE_GAP = 150  # Increase the gap between the pipes
PIPE_VELOCITY = 8

# Ground dimensions
GROUND_HEIGHT = 100

# Colors
BACKGROUND_COLOR = (0, 0, 0)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
SCORE_COLOR = (255, 255, 255)
GROUND_COLOR = (128, 128, 128)

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for managing the frame rate
clock = pygame.time.Clock()

# Load bird image
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Load background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.gravity = 0.9
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = -12

    def reset_position(self):
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        window.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x, gap_height):
        self.x = x
        self.gap_height = gap_height
        self.passed = False

    def update(self):
        self.x -= PIPE_VELOCITY

    def draw(self):
        pygame.draw.rect(window, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.gap_height))
        pygame.draw.rect(window, PIPE_COLOR, (self.x, self.gap_height + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_height), pygame.Rect(self.x, self.gap_height + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT)

# Main menu function
def main_menu():
    global start_flag, game_over_flag, score
    start_flag = False
    game_over_flag = False
    score = 0

    # Clear the list of pipes
    pipes.clear()

    # Reset bird position
    bird.reset_position()

    # Display main menu instructions
    instructions_text1 = font.render("Press SPACE to start", True, SCORE_COLOR)
    instructions_text2 = font.render("Use SPACE to jump", True, SCORE_COLOR)
    window.blit(instructions_text1, (WINDOW_WIDTH // 2 - instructions_text1.get_width() // 2, WINDOW_HEIGHT // 2 - instructions_text1.get_height() * 2))
    window.blit(instructions_text2, (WINDOW_WIDTH // 2 - instructions_text2.get_width() // 2, WINDOW_HEIGHT // 2 - instructions_text2.get_height() // 2))

    pygame.display.flip()

# Game over function
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))

    # Display score
    score_text = font.render("Score: " + str(score), True, SCORE_COLOR)
    window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))

    # Update high score
    if score > high_score:
        high_score_file = open("highscore.txt", "w")
        high_score_file.write(str(score))
        high_score_file.close()
        high_score_text = font.render("New High Score: " + str(score), True, SCORE_COLOR)
        window.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + high_score_text.get_height() * 2))

    pygame.display.flip()
    pygame.time.wait(2000)
    main_menu()

# Load high score
high_score = 0
try:
    high_score_file = open("highscore.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
except FileNotFoundError:
    pass

# Create bird object
bird = Bird()

# List to hold pipes
pipes = []

# Timer event for adding pipes
ADDPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPIPE, 1500)

# Game over flag
game_over_flag = False

# Start flag
start_flag = False

# Score
score = 0

# Load font
font = pygame.font.Font(None, 36)

# Game loop
background_x = 0  # Initialize background x-coordinate
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not start_flag and not game_over_flag:
                    start_flag = True
                elif game_over_flag:
                    main_menu()
                bird.jump()

        if event.type == ADDPIPE and not game_over_flag and start_flag:
            gap_height = random.randint(50, WINDOW_HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)
            new_pipe = Pipe(WINDOW_WIDTH, gap_height)
            pipes.append(new_pipe)

    # Update bird position and pipes
    if start_flag:
        bird.update()

    for pipe in pipes:
        pipe.update()
        if pipe.x + PIPE_WIDTH < 0:
            pipes.remove(pipe)

        if pipe.x + PIPE_WIDTH < bird.x:
            if not pipe.passed:
                pipe.passed = True
                score += 1

        bird_rect = pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)
        upper_pipe_rect, lower_pipe_rect = pipe.get_rect()

        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            game_over_flag = True

    # Check if bird hits the ground
    if bird.y + BIRD_HEIGHT >= WINDOW_HEIGHT - GROUND_HEIGHT:
        game_over_flag = True

    # Update background position
    background_x -= 1  # Move the background by 1 pixel to the left

    # Draw background
    window.blit(background_image, (background_x, 0))
    window.blit(background_image, (background_x + WINDOW_WIDTH, 0))  # Draw a second background image next to the first one

    # Reset background position when it goes off-screen
    if background_x <= -WINDOW_WIDTH:
        background_x = 0

    # Draw ground
    pygame.draw.rect(window, GROUND_COLOR, (0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT))

    # Draw bird only when the game has started
    if start_flag:
        bird.draw()

    # Draw pipes
    for pipe in pipes:
        pipe.draw()

    # Draw score
    score_text = font.render("Score: " + str(score), True, SCORE_COLOR)
    window.blit(score_text, (10, 10))

    # Draw high score
    high_score_text = font.render("High Score: " + str(high_score), True, SCORE_COLOR)
    window.blit(high_score_text, (10, 50))

    # Show game over screen
    if game_over_flag:
        game_over()

    # Show main menu screen
    if not start_flag and not game_over_flag:
        main_menu()

    # Update the display
    pygame.display.update()
    clock.tick(30)
