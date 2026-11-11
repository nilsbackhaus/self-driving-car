import pygame
import math

from classes.sensor import Sensor
from constants.car_c import *

class Car:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height

        self.sensor = Sensor(self)
        self.checkpoint_reached = 0
        self.lap_count = 0
        self.first_checkpoint_progress = 0.0
        self.stopped_frames = 0

        self.speed = 0.0
        self.angle = 0.0
        self.acceleration = ACCELERATION
        self.friction = FRICTION
        self.maximum_speed = MAXIMUM_SPEED

        self.color = CAR_COLOR
        self.start_position()

    def start_position(self):
        self.rect = self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill(pygame.Color(self.color))
        
    def update_position(self, track_mask: pygame.Mask):
        self.x -= self.speed * math.sin(self.angle)
        self.y -= self.speed * math.cos(self.angle)

        self.rect = self.surf.get_rect(center=(self.x, self.y))

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

    def check_collision(self, track_mask: pygame.Mask):
        rotated = pygame.transform.rotozoom(self.surf, math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        car_mask = pygame.mask.from_surface(rotated)
        if track_mask.overlap(car_mask, rect.topleft) is not None:
            return True

    def check_checkpoint(self, checkpoints: list):
        for checkpoint in checkpoints:
            if self.rect.colliderect(checkpoint.rect):
                if checkpoint.id == 1 and self.checkpoint_reached == len(checkpoints):
                    self.lap_count += 1
                    self.checkpoint_reached = 1
                elif checkpoint.id == (self.checkpoint_reached + 1):
                    self.checkpoint_reached = checkpoint.id

    def update_first_checkpoint_progress(self, checkpoint):
        if self.checkpoint_reached:
            return

        target = checkpoint.rect.center
        start_distance = math.hypot(self.start_x - target[0], self.start_y - target[1])
        distance = math.hypot(self.x - target[0], self.y - target[1])
        if start_distance:
            progress = max(0.0, min(0.99, 1 - distance / start_distance))
            self.first_checkpoint_progress = max(self.first_checkpoint_progress, progress)
                


    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotozoom(self.surf, math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        screen.blit(rotated, rect)
        # self.sensor.draw(screen)
