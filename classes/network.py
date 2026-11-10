import pygame
import numpy as np
import math
import random

from classes.car import Car
from constants import network_c as network_constants

class Element:
    def __init__(self):
        self.car = Car(120, 400, 15, 30)

        self.input_weights = (0.10 * np.random.randn(self.car.sensor.ray_count, network_constants.N_OF_HIDDEN_LAYER_NEURONS))
        self.input_biases = np.zeros((1, network_constants.N_OF_HIDDEN_LAYER_NEURONS))

        self.hidden_layer1_weights = (0.10 * np.random.randn(network_constants.N_OF_HIDDEN_LAYER_NEURONS, network_constants.N_OF_HIDDEN_LAYER_NEURONS))
        self.hidden_layer1_biases = np.zeros((1, network_constants.N_OF_HIDDEN_LAYER_NEURONS))

        self.hidden_layer2_weights = (0.10 * np.random.randn(network_constants.N_OF_HIDDEN_LAYER_NEURONS, network_constants.N_OF_POSSIBLE_OUTPUTS))
        self.hidden_layer2_biases = np.zeros((1, network_constants.N_OF_POSSIBLE_OUTPUTS))

    def feed_forward(self, inputs, weights, biases):
        self.output = np.dot(inputs, weights) + biases

    def activation_ReLU(self, inputs):
        self.output = np.maximum(0, inputs)

    def choose_game_input(self):
        input = None

        self.feed_forward(self.car.sensor.readings, self.input_weights, self.input_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer1_weights, self.hidden_layer1_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer2_weights, self.hidden_layer2_biases)
        print(self.output)
        
        return random.randint(0, network_constants.N_OF_POSSIBLE_OUTPUTS)

    def crossbreed(self):
        pass