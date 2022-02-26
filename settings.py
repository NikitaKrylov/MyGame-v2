import os
import os
import logging

version = 'ALPHA'

APP_NAME = 'Game'
LOGGERLEVEL = logging.INFO
PATH = os.getcwd()
MEDIA = PATH + '\\media'
IMAGES = MEDIA + '\\images'
CONTROL_CONFIG = PATH + '\\control_config.json'


"""COLORS"""

PLAYER_HEALTHBAR_BACKGROUND_COLOR = (198, 212, 217)
PLAYER_HEALTHBAR_COLOR = (240, 84, 84)
ENEMY_HEALTHBAR_COLOR = (240, 45, 45)
