import sys
import pygame

from classes.player import Player
from constants import clock as clock_constants
from constants import player as player_constants
from constants import pygame as screen_constants

pygame.init()

screen = pygame.display.set_mode((screen_constants.WIDTH, screen_constants.HEIGHT), vsync = 1)
pygame.display.set_caption("Self-driving Car")

player = Player((screen_constants.WIDTH // 6), (screen_constants.HEIGHT // 2), 20, 40)
track = pygame.image.load("assets/track.png").convert_alpha()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_angle: int | float = player_constants.ANGLE_INCREMENT * (player.speed / player_constants.TURNING_POWER)
    
    if keys[pygame.K_w]:
        player.speed += player.acceleration
    elif keys[pygame.K_s]:
        player.speed -= player.acceleration

    if keys[pygame.K_a]:
        player.angle += float(new_angle)
    elif keys[pygame.K_d]:
        player.angle -= float(new_angle)

    player.update_position()
    
    screen.fill(screen_constants.SCREEN_COLOR)
    screen.blit(track, (0, 0))
    player.draw(screen)
    pygame.display.flip()

    clock.tick(clock_constants.FPS) 

pygame.quit()
sys.exit()