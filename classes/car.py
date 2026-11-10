import pygame
import math

from classes.sensor import Sensor
from constants import car_c as car_constants

class Car:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.sensor = Sensor(self)
        self.checkpoint_reached = 0
        self.lap_count = 0

        self.speed = 0.0
        self.angle = 0.0
        self.acceleration = car_constants.ACCELERATION
        self.friction = car_constants.FRICTION
        self.maximum_speed = car_constants.MAXIMUM_SPEED

        self.color = car_constants.CAR_COLOR
        self.start_position()

    def start_position(self):
        self.rect = self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill(pygame.Color(self.color))
        
    def update_position(self, track_mask):
        self.x -= self.speed * math.sin(self.angle)
        self.y -= self.speed * math.cos(self.angle)

        self.rect = self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction

        if self.speed > self.maximum_speed:
            self.speed = self.maximum_speed
        elif self.speed < -self.maximum_speed:
            self.speed = -self.maximum_speed

        if abs(self.speed) < self.friction:
            self.speed = 0.0

        self.sensor.update(track_mask)

    def check_collision(self, track_mask):
        rotated = pygame.transform.rotozoom(self.surf, math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        car_mask = pygame.mask.from_surface(rotated)
        if track_mask.overlap(car_mask, rect.topleft) is not None:
            return True

    def check_checkpoint(self, checkpoints):
        for checkpoint in checkpoints:
            if self.rect.colliderect(checkpoint.rect):
                if checkpoint.id > self.checkpoint_reached:
                    self.checkpoint_reached = checkpoint.id

                    if self.checkpoint_reached == len(checkpoints):
                        self.checkpoint_reached = 1
                        self.lap_count += 1

                print(self.checkpoint_reached)
                print(self.lap_count)


    def draw(self, screen):
        rotated = pygame.transform.rotozoom(self.surf, math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        screen.blit(rotated, rect)
        self.sensor.draw(screen)
