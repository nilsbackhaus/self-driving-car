import pygame

import constants.road as road_constants

class Road:
    def __init__(self, x: int, width: int, lane_count: int = 3):
        self.x = x
        self.width = width
        self.lane_count = lane_count
        self.top = -road_constants.INFINITY
        self.bottom = road_constants.INFINITY

    def draw(self, screen):
        screen_rect = screen.get_rect()
        pygame.draw.line(screen, road_constants.ROAD_COLOR, (0, 0), (0, screen_rect.height), 10)
        pygame.draw.line(screen, road_constants.ROAD_COLOR, (self.width, 0), (self.width, screen_rect.height), 10)
