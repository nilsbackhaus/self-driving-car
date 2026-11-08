import pygame
import math

from constants import player as player_constants

class Player:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.speed = 0.0
        self.angle = float(math.pi)
        self.acceleration = player_constants.ACCELERATION
        self.friction = player_constants.FRICTION
        self.maximum_speed = player_constants.MAXIMUM_SPEED

        self.color = player_constants.PLAYER_COLOR
        self.start_position()

    def start_position(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill(pygame.Color(self.color))
        
    def update_position(self):
        self.x -= self.speed * math.sin(self.angle)
        self.y -= self.speed * math.cos(self.angle)

        self.rect = (self.x, self.y, self.width, self.height)

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

    def draw(self, screen):
        rotated = pygame.transform.rotozoom(self.surf, math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        screen.blit(rotated, rect)
