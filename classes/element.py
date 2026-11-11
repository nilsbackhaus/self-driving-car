import pygame
import numpy as np
import math
import random

from classes.car import Car
from constants.element_c import *
from constants.training_c import *

def mutation_chance(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.random() < MUTATION_CHANCE:
                weights[i][j] += random.uniform(-MUTATION_CHANGE, MUTATION_CHANGE)

def random_select(weights1, weights2, child_weights):
    for i in range(len(weights1)):
        for j in range(len(weights1[i])):
            if random.choice([0, 1]):
                child_weights[i][j] = weights1[i][j]
            else:
                child_weights[i][j] = weights2[i][j]

def generate_breeding_pool(elements: list, n_of_checkpoints: int):
    breeding_pool = []
    
    for element in elements:
        fitness = element.car.lap_count * (n_of_checkpoints - 1) + element.car.checkpoint_reached
        if fitness == 0:
            fitness = element.car.first_checkpoint_progress
        for _ in range(math.floor(fitness * 100 / FITNESS_PER_POOL_ENTRY)):
            breeding_pool.append(element)

    return breeding_pool

def breed_new_population(breeding_pool: list):
    new_population = []

    for _ in range(AMOUNT_OF_CARS):
        parent1 = random.choice(breeding_pool)
        parent2 = random.choice(breeding_pool)
        child = parent1.breed(parent2)
        new_population.append(child)

    return new_population

def mutate_population(elements: list):
    for element in elements:
        mutation_chance(element.input_weights)
        mutation_chance(element.input_biases)
        mutation_chance(element.hidden_layer1_weights)
        mutation_chance(element.hidden_layer1_biases)
        mutation_chance(element.hidden_layer2_weights)
        mutation_chance(element.hidden_layer2_biases)

class Element:
    def __init__(self):
        self.car = Car(120, 450, 15, 30)

        self.input_weights = (0.10 * np.random.randn(self.car.sensor.ray_count, N_OF_HIDDEN_LAYER_NEURONS))
        self.input_biases = np.full((1, N_OF_HIDDEN_LAYER_NEURONS), random.uniform(0.01, 0.1))

        self.hidden_layer1_weights = (0.10 * np.random.randn(N_OF_HIDDEN_LAYER_NEURONS, N_OF_HIDDEN_LAYER_NEURONS))
        self.hidden_layer1_biases = np.full((1, N_OF_HIDDEN_LAYER_NEURONS), random.uniform(0.01, 0.1))

        self.hidden_layer2_weights = (0.10 * np.random.randn(N_OF_HIDDEN_LAYER_NEURONS, N_OF_POSSIBLE_OUTPUTS))
        self.hidden_layer2_biases = np.full((1, N_OF_POSSIBLE_OUTPUTS), random.uniform(0.01, 0.1))

    def feed_forward(self, inputs: list[float] | np.ndarray, weights: np.ndarray, biases: np.ndarray):
        self.output = np.dot(inputs, weights) + biases

    def activation_ReLU(self, inputs: np.ndarray):
        self.output = np.maximum(0, inputs)

    def choose_game_input(self):
        if len(self.car.sensor.readings) != self.car.sensor.ray_count:
            return 0

        self.feed_forward(self.car.sensor.readings, self.input_weights, self.input_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer1_weights, self.hidden_layer1_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer2_weights, self.hidden_layer2_biases)
        
        return int(np.argmax(self.output))

    def crossbreed(self):
        pass

    def breed(self, partner):
        child = Element()
        random_select(self.input_weights, partner.input_weights, child.input_weights)
        random_select(self.input_biases, partner.input_biases, child.input_biases)
        random_select(self.hidden_layer1_weights, partner.hidden_layer1_weights, child.hidden_layer1_weights)
        random_select(self.hidden_layer1_biases, partner.hidden_layer1_biases, child.hidden_layer1_biases)
        random_select(self.hidden_layer2_weights, partner.hidden_layer2_weights, child.hidden_layer2_weights)
        random_select(self.hidden_layer2_biases, partner.hidden_layer2_biases, child.hidden_layer2_biases)
        return child
               
