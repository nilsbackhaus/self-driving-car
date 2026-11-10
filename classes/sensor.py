import pygame
import math

from utils.math import *
from constants.sensor_c import *

class Sensor:
    def __init__(self, car):
        self.car = car
        self.ray_count = RAY_COUNT
        self.ray_length = RAY_LENGTH
        self.ray_spread = RAY_SPREAD

        self.rays = []
        self.readings = []

    def update(self, track_mask: pygame.Mask):
        self.rays = []
        self.readings = []
        self.cast_rays(track_mask)

    def cast_rays(self, track_mask: pygame.Mask):
        for i in range(self.ray_count):
            ray_angle = lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                i / (self.ray_count - 1)
            ) + self.car.angle

            start = (self.car.x, self.car.y)
            direction = (-math.sin(ray_angle), -math.cos(ray_angle))
            end = (
                self.car.x - math.sin(ray_angle) * self.ray_length,
                self.car.y - math.cos(ray_angle) * self.ray_length
                )

            for i in range(0, int(self.ray_length), PIXEL_PER_STEP):
                point = ((start[0] + direction[0] * i), (start[1] + direction[1] * i))
                reading = 0

                if 0 <= point[0] < track_mask.get_size()[0] and 0 <= point[1] < track_mask.get_size()[1]:
                    if track_mask.get_at(point):
                        end = point
                        reading = (i / self.ray_length)
                        break

                    if reading == 0:
                        reading = 1


            self.rays.append((start, end))
            self.readings.append(reading)

    def draw(self, screen: pygame.Surface):
        for i in range(self.ray_count):
            pygame.draw.line(screen, RAY_COLOR, self.rays[i][0], self.rays[i][1], 2)
