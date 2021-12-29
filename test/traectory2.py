import pygame as pg
import sys
import os
from math import sin
import pygame.gfxdraw


pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    display.fill((249, 255, 190))
    pg.gfxdraw.box(display, pg.Rect(100, 100, 100, 100), (255, 0, 0, 90), border_radius=10)

    pg.display.update()
    clock.tick(60)
