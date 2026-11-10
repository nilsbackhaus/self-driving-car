from constants.clock_c import *

def validate_s_with_fps(seconds: int | float):
    return float(seconds * FPS)

def validate_m_with_fps(minutes: int | float):
    return validate_s_with_fps(minutes * 60)