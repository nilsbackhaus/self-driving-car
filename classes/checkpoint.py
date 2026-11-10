import pygame

from constants.checkpoint_c import *

class Checkpoint:
    def __init__(self, x: int, y: int, width: int, height: int, id: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.id = id

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, CHECKPOINT_COLOR, self.rect)