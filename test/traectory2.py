import pygame as pg
import sys
import os
from math import sin

from pygame.draw import line

pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()
xcord = [i for i in range(1300)]
ycord = [int(sin(i/20)*50)+500 for i in xcord]
image = pg.image.load(os.getcwd()+'\media\images\enemy\what\hui2.png')
image = pg.transform.scale(image, (image.get_width()*4, image.get_height()*4))

rect = image.get_rect(center=(450, 650))

cords = list(zip(xcord, ycord))


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    display.fill((249, 255, 190))
    pg.draw.lines(display, (255, 0, 0), False, cords)
    display.blit(image, rect)

    pg.display.update()
    clock.tick(60)
