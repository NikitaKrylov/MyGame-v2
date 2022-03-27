import os
import os
import logging
import ctypes

version = 'ALPHA'

APP_NAME = 'Game'
LOGGERLEVEL = logging.INFO
PATH = os.getcwd()
MEDIA = PATH + '\\media'
IMAGES = MEDIA + '\\images'
CONTROL_CONFIG = PATH + '\\control_config.json'

"""SIZES"""
user32 = ctypes.windll.user32
WINDOW_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
DISPLAY_SIZE = [int(0.4*WINDOW_SIZE[0]), int(0.9*WINDOW_SIZE[1])]


"""COLORS"""

PLAYER_HEALTHBAR_BACKGROUND_COLOR = (198, 212, 217)
PLAYER_HEALTHBAR_COLOR = (240, 84, 84)
ENEMY_HEALTHBAR_COLOR = (240, 45, 45)
