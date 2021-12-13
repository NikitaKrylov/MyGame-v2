import pygame as pg
import sys
from pygame.sprite import Sprite


class SP(Sprite):
    def __init__(self, cord_list):
        self.color = [0, 230, 190]
        self.cord_list = cord_list
        self.iteration = 0
        self.last = 0

    def draw(self, display):
        pg.draw.circle(display, self.color, self.cord_list[self.iteration], 10)

    def update(self, now):
        if now - self.last >= 30:
            self.last = now

            if self.iteration < len(self.cord_list)-1:
                self.iteration += 1


pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()
cord_list = []
mouseDown = False
spr = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == 113:
                cord_list.clear()
                if spr:
                    spr = None

            elif event.key == 101:
                spr = SP(cord_list)

            else:
                print(event.key)

        if event.type == pg.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pg.MOUSEBUTTONUP:
            mouseDown = False

        if mouseDown:
            if event.type == pg.MOUSEMOTION:
                cord_list.append(event.pos)

    display.fill((249, 255, 190))
    if len(cord_list) > 1:
        # pg.draw.lines(display, (255, 0, 0), False, cord_list, width=2)

        if spr:
            spr.update(pg.time.get_ticks())
            spr.draw(display)

    pg.display.update()
    clock.tick(60)
