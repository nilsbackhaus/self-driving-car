import pygame
import numpy
import math
import random

from classes.car import Car

class Element:
    def __init__(self):
        self.car = Car(150, 200, 15, 30)

    def feed_forward(self):
        pass

    def activation_ReLU(self):
        pass

    def choose_game_input(self):
        return random.randint(0, 4)

    def crossbreed(self):
        pass