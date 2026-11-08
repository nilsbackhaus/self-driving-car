import pygame
import math

def lerp(A: float, B: float, t: float):
    return A + (B - A) * t