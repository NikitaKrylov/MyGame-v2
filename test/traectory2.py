import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN
from pygame.sprite import Sprite, Group, spritecollide
import sys
import os
import random
from math import sin, sqrt
import pygame.gfxdraw


def sign(value):
    return 1 if value > 0 else -1


class Shell(Sprite):
    default_speed = 1600
    speed = default_speed

    def __init__(self, center: list, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((20, 20))
        self.image.fill((0, 100, 255))
        self.rect = self.image.get_rect(center=center)
        self.direction = pg.Vector2(1, 0).rotate(random.randint(0, 360))

    def draw(self, display, *args, **kwargs):
        display.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        player_cord = kwargs.get('player_cord')

        dx, dy = player_cord[0] - \
            self.rect.centerx, player_cord[1] - self.rect.centery
        distanse = sqrt(dx**2 + dy**2)
        self.direction.update(dx/distanse, dy/distanse)

        if distanse > 1000:
            self.speed = 0
        else:
            self.speed = round(self.default_speed / distanse)

        self.rect.centerx += self.direction.x*self.speed
        self.rect.centery += self.direction.y*self.speed

        # self.rect.centerx += dx/distanse*self.speed
        # self.rect.centery += dy/distanse*self.speed

        if self.rect.top > 1300 or self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > 900 or self.rect.right < 0:
            self.kill()


class Player(Sprite):
    def __init__(self, center: list, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((100, 100))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=center)

    def draw(self, display, *args, **kwargs):
        display.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        self.rect.center = pg.mouse.get_pos()


pg.init()
display = pg.display.set_mode((900, 1300))
clock = pg.time.Clock()
player = Player((450, 100))
shellGroup = Group()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            Shell((100, 100), shellGroup)

    display.fill((249, 255, 190))
    player.update()
    player.draw(display)
    shellGroup.update(player_cord=player.rect.center)
    shellGroup.draw(display)

    spritecollide(player, shellGroup, True)

    pg.display.update()
    clock.tick(60)
