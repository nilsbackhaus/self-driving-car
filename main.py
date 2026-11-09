import sys
import pygame

from classes.car import Car
from constants import clock as clock_constants
from constants import car as car_constants
from constants import pygame as screen_constants

pygame.init()

screen = pygame.display.set_mode((screen_constants.WIDTH, screen_constants.HEIGHT), vsync = 1)
pygame.display.set_caption("Self-driving Car")

clock = pygame.time.Clock()
car = Car((screen_constants.WIDTH // 6), (screen_constants.HEIGHT // 2), 20, 40)
track = pygame.image.load("assets/track.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_angle: int | float = car_constants.ANGLE_INCREMENT * (car.speed / car_constants.TURNING_POWER)
    
    if keys[pygame.K_w]:
        car.speed += car.acceleration
    elif keys[pygame.K_s]:
        car.speed -= car.acceleration

    if keys[pygame.K_a]:
        car.angle += float(new_angle)
    elif keys[pygame.K_d]:
        car.angle -= float(new_angle)

    car.update_position()
    print(car.check_collision(track_mask))
    
    screen.fill(screen_constants.SCREEN_COLOR)
    screen.blit(track, (0, 0))
    car.draw(screen)
    pygame.display.flip()

    clock.tick(clock_constants.FPS) 

pygame.quit()
sys.exit()