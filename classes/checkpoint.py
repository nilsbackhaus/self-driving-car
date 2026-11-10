import pygame
import numpy as np

from constants import checkpoint_c as checkpoint_constants

class Checkpoint:
    def __init__(self, x: int, y: int, width: int, height: int, id: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.id = id

    def draw(self, screen):
        pygame.draw.rect(screen, checkpoint_constants.CHECKPOINT_COLOR, self.rect)