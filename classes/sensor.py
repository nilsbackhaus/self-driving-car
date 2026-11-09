import pygame
import math

from utils.math import *

class Sensor:
    def __init__(self, car):
        self.car = car
        self.ray_count = 3
        self.ray_length = 100
        self.ray_spread = math.pi / 4
        self.rays = []

    def update(self):
        self.rays = []
        for i in range(self.ray_count):
            ray_angle = lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                i / (self.ray_count - 1)
            )

            start = (self.car.x, self.car.y)
            end = (
                self.car.x - math.sin(ray_angle) * self.ray_length,
                self.car.y - math.cos(ray_angle) * self.ray_length
                )

            self.rays.append((start, end))

    def draw(self, screen):
        for i in range(self.ray_count):
            pygame.draw.line(screen, "YELLOW", self.rays[i][0], self.rays[i][1], 2)
