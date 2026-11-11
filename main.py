import pygame, sys

from classes.checkpoint import Checkpoint
from classes.element import *

from utils.time import *
from constants.clock_c import *
from constants.car_c import *
from constants.pygame_c import * 
from constants.training_c import *

pygame.init()

py_clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
track = pygame.image.load("assets/track.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

checkpoints = []
elements = []
crashed_elements = []

def update_all_cars():
    for element in elements:
        new_angle = float(ANGLE_INCREMENT * (element.car.speed / TURNING_POWER))
    
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
    
    for element in elements[:]:
        element.car.update_position(track_mask)
        element.car.update_first_checkpoint_progress(checkpoints[0])

        if abs(element.car.speed) < 0.01:
            element.car.stopped_frames += 1
        else:
            element.car.stopped_frames = 0

        if element.car.check_collision(track_mask) or element.car.stopped_frames >= 3 * FPS:
            crashed_elements.append(element)
            elements.remove(element)
            continue

        element.car.check_checkpoint(checkpoints)
        element.car.draw(screen)

def reward_train():
    global elements

    breeding_pool = generate_breeding_pool(elements + crashed_elements, len(checkpoints))
    crashed_elements.clear()

    if not breeding_pool:
        elements = []
        for _ in range(AMOUNT_OF_CARS):
            elements.append(Element())
    else:
        elements = breed_new_population(breeding_pool)
        mutate_population(elements)
    
def train():
    training_timer: float = VALIDATED_TRAINING_DURATION
    last_progress: int = -1
    running: bool = True

    while running:
        if training_timer < 0:
            running = False

        if not elements:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #    print(pygame.mouse.get_pos())

        training_timer -= float(1)
        
        progress = int((VALIDATED_TRAINING_DURATION - training_timer) / VALIDATED_TRAINING_DURATION * 100)
        if progress != last_progress:
            print(f"Training progress: {progress}%")
            last_progress = progress

        screen.fill(SCREEN_COLOR)
        screen.blit(track, (0, 0))

        update_all_cars()

        pygame.display.flip()
        py_clock.tick(FPS)

    if last_progress == 100:
        print(f"Training has completed. Trained for {TRAINING_DURATION} minute(s).")
    else:
        print("Training was interrupted.")

    return True

def init():
    global checkpoints, elements

    checkpoints = [
        Checkpoint(55, 280, 200, 10, 1), Checkpoint(230, 50, 10, 200, 2),
        Checkpoint(400, 140, 10, 200, 3), Checkpoint(570, 320, 200, 10, 4),
        Checkpoint(510, 400, 10, 200, 5), Checkpoint(251, 400, 10, 200, 6),
    ]

    for _ in range(AMOUNT_OF_CARS):
        elements.append(Element())

    for _ in range(TRAINING_ITERATION):
        if not train():
            break

        reward_train()

    pygame.quit()
    sys.exit()

init()

