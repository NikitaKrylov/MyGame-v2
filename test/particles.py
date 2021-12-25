import pygame as pg
import sys
from pygame.sprite import Sprite
import sys
from math import pi
import random

# # sys.getsizeof


pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            pass


    display.fill((0, 0, 0))

    pg.display.update()
    clock.tick(60)
