import pygame
import numpy as np
import math
import random

from classes.car import Car
from constants import network_c as network_constants

class Element:
    def __init__(self):
        self.car = Car(120, 400, 15, 30)

        self.weights = (0.10 * np.random.randn(self.car.sensor.ray_count, network_constants.N_OF_HIDDEN_LAYER_NEURONS))
        self.biases = np.zeros((1, network_constants.N_OF_HIDDEN_LAYER_NEURONS))

    def feed_forward(self):
        pass

    def activation_ReLU(self):
        pass

    def choose_game_input(self):
        return random.randint(0, 4)

    def crossbreed(self):
        pass