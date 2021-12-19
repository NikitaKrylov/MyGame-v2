import pygame as pg
import sys
from pygame.sprite import Sprite
import sys
from math import pi
import random

# # sys.getsizeof


class Particles:
    def __init__(self):
        self._particles = []  # [pos:list, direction:Vector, radius:int]
        self.velocity = 7
        self.size = [6, 15]
        self.step = 0.8

    def draw(self, display):
        for particle in self._particles:
            # pg.draw.circle(display, (250, 250, 250), particle[0], particle[2])
            pg.draw.rect(display, (57, 190, 247), pg.Rect(
                particle[0][0]-particle[2]/2, particle[0][1]-particle[2]/2, particle[2], particle[2]))

    def update(self):
        if self._particles:
            self.remove()
            for particle in self._particles:
                particle[0][0] += particle[1].x * self.velocity
                particle[0][1] += particle[1].y * self.velocity
                particle[2] -= self.step

    def remove(self):
        for particle in self._particles:
            if particle[2] <= 5:
                self._particles.remove(particle)

    def create(self, pos):
        for i in range(20):
            direction = pg.Vector2(1, 0).rotate_rad(
                random.uniform(0.0, pi*2))
            self._particles.append(
                [list(pos), direction, random.uniform(*self.size)])


pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()
particles = Particles()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            pass

        if event.type == pg.MOUSEBUTTONDOWN:
            particles.create(event.pos)

    display.fill((0, 0, 0))
    particles.draw(display)
    particles.update()

    pg.display.update()
    clock.tick(60)
