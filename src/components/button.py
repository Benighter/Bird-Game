import pygame
from ..utils.constants import SCORE_COLOR

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, self.hover_color, button_rect)
        else:
            pygame.draw.rect(window, self.color, button_rect)

        text_surface = self.font.render(self.text, True, SCORE_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] 