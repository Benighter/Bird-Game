import pygame
from ..utils.constants import PIPE_WIDTH, PIPE_COLOR, PIPE_GAP, PIPE_VELOCITY, WINDOW_HEIGHT

class Pipe:
    def __init__(self, x, gap_height):
        self.x = x
        self.gap_height = gap_height
        self.passed = False

    def update(self):
        self.x -= PIPE_VELOCITY

    def draw(self, window):
        pygame.draw.rect(window, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.gap_height))
        pygame.draw.rect(window, PIPE_COLOR, (self.x, self.gap_height + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_height), pygame.Rect(self.x, self.gap_height + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT) 