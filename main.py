import sys
import pygame

from classes.checkpoint import Checkpoint
from classes.element import Element
from constants import clock_c as clock_constants
from constants import car_c as car_constants
from constants import pygame_c as screen_constants

pygame.init()

elements = []
for i in range(10):
    elements.append(Element())

checkpoints = [
    Checkpoint(55, 280, 200, 10, 1), Checkpoint(230, 50, 10, 200, 2),
    Checkpoint(400, 140, 10, 200, 3), Checkpoint(570, 320, 200, 10, 4),
    Checkpoint(510, 400, 10, 200, 5), Checkpoint(251, 400, 10, 200, 6),
]

screen = pygame.display.set_mode((screen_constants.WIDTH, screen_constants.HEIGHT), vsync = 1)
pygame.display.set_caption("Self-driving Car")

track = pygame.image.load("assets/track.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        print(pygame.mouse.get_pos())

    screen.fill(screen_constants.SCREEN_COLOR)

    for checkpoint in checkpoints:
        checkpoint.draw(screen)

    screen.blit(track, (0, 0))

    keys = pygame.key.get_pressed()

    for element in elements:
        new_angle = float(car_constants.ANGLE_INCREMENT * (element.car.speed / car_constants.TURNING_POWER))

        match element.choose_game_input():
            case 0: # Forward
                element.car.speed += element.car.acceleration
            case 1: # Forward + Left
                element.car.speed += element.car.acceleration
                element.car.angle -= new_angle
            case 2: # Forward + Right
                element.car.speed += element.car.acceleration
                element.car.angle += new_angle
            case 3: # Right
                element.car.angle -= new_angle
            case 4: # Left
                element.car.angle += new_angle

    for i, element in enumerate(elements):
        element.car.update_position(track_mask)
        if element.car.check_collision(track_mask):
            elements.pop(i)

        element.car.check_checkpoint(checkpoints)
        element.car.draw(screen)

    pygame.display.flip()
    clock.tick(clock_constants.FPS) 

pygame.quit()
sys.exit()