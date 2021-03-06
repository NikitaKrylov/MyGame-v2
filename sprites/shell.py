from math import sin, pi, cos
from matplotlib.pyplot import spring
import pygame as pg
from pygame.sprite import Sprite, AbstractGroup
from scipy import rand
from animation import Animator
from animation import StaticMovement, Animator
import random

from logger.logger import get_logger
from .particle import Particle, ParticleShell

log = get_logger(__name__)
# ----------------------------------BASE SHELL---------------------------------------------


class BaseShell(Sprite):
    isPlayer: bool = None
    animation = Animator
    _damage = 10
    _speed = 20

    def __init__(self, images: list,  pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(*groups)
        self.particle_group = particle_group
        self.animation = self.animation()
        self.images = images
        self.image = images[0]
        self.movement = StaticMovement(pg.Vector2(0.0, -1.0))
        """Изображение, которое должно рисоваться в данный момент,
        должно быть названо image для нормальной работы группы
        """
        self.rect = self.image.get_rect(center=pos)
        self.rects = [self.rect]

    def update(self, *args, **kwargs):
        self.movement.update(
            self.rect,
            self.rects,
            speed=self._speed
        )

        if self.rect.bottom < -self.rect.bottom:
            super().kill()
        elif self.rect.top > kwargs.get('display_size')[1]:
            super().kill()

        return super().update(*args, **kwargs)

    def getDamage(self):
        damage = self._damage
        self.kill()
        return damage

    def draw(self, display):
        return display.blit(self.image, self.rect)

    def kill(self):
        return super().kill()


# For the shell to hit the area you need to inherit your shell class from IAreaShell class
# It has an _area fielad which stores an area size and position
class IAreaShell:
    _area: pg.Rect = None

    def GetArea(self):
        return self._area

    def SetArea(self, rect: pg.Rect):
        if not isinstance(rect, pg.Rect):
            return log.error("given argement 'rect' must be Rect class")
        self._area = rect

    def CollideGroup(self, group: AbstractGroup):
        collide_list = []

        for sprite in group.sprites():
            for rect in sprite.rects:
                if self.GetArea().colliderect(rect):
                    collide_list.append(sprite)
                    continue

        return collide_list

    def __repr__(self):
        return f' AreaShell - {self._area}'

# ----------------------------------PLAYER SHELL---------------------------------------------


class Strike(BaseShell, IAreaShell):
    _damage = 300
    _speed = 0
    _area = pg.Rect(0, 0, 300, 300)

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.GetArea().center = pos
        self.movement.direction = pg.Vector2(0, 0)

    def getDamage(self):
        return self._damage

    def kill(self):
        colors = [(255, 0, 0), (255, 140, 0), (255, 90, 0),
                  (217, 114, 17), (245, 96, 10), (255, 30, 0)]
        for _ in range(70):
            alpha = random.random() * 2 * pi
            pos = [int(self.rect.centerx + self.rect.width*0.2 * cos(alpha)),
                   int(self.rect.centery + self.rect.height*0.2 * sin(alpha))]
            vector = pg.Vector2(0, -1).rotate(random.randint(0, 360))
            self.particle_group.add(Particle(
                pos=pos,
                size=random.randint(2, int(self.rect.width*0.2)),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(
                    int(self.rect.width*0.3), int(self.rect.width*0.7)),
                size_rate=random.uniform(.5, 2),
                speed_rate=-random.uniform(.05, .3),
                shape='square'))

        for _ in range(200):
            alpha = random.random() * 2 * pi
            pos = [int(self.rect.centerx + self.rect.width/2 * cos(alpha)),
                   int(self.rect.centery + self.rect.height/2 * sin(alpha))]
            vector = pg.Vector2(0, -1).rotate(random.randint(0, 360))
            self.particle_group.add(Particle(
                pos=pos,
                size=random.randint(2, int(self.rect.width*0.2)),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(
                    int(self.rect.width*0.1), int(self.rect.width*0.6)),
                size_rate=random.uniform(1, 4),
                speed_rate=-random.uniform(.05, .3),
                shape='square'))
        return super().kill()


# ----------------------------------------------------------------------------------------

class FirstShell(BaseShell):
    _damage = 25
    _speed = 20

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.rects = [pg.Rect(self.rect.x + self.rect.width * 0.15, self.rect.y +
                              self.rect.height * 0.15, self.rect.width*0.7, self.rect.height*0.7)]

    def kill(self):
        """create particles when sprite die"""
        colors = [(170, 238, 255), (127, 233, 247), (180, 248, 255)]
        for i in range(9):
            vector = pg.Vector2(1, 0).rotate(random.randint(1, 359))
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=random.randint(6, int(self.rect.width/2)),
                speed=random.randint(8, 12),
                color=random.choice(colors),
                vector=vector,
                life_size=5,
                speed_rate=-0.3,
                size_rate=-0.5))
        return super().kill()


class RedShell(BaseShell):
    _damage = 17
    _speed = 19

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.rects = [pg.Rect(self.rect.x + self.rect.width * 0.3, self.rect.y +
                              self.rect.height * 0.3, self.rect.width*0.6, self.rect.height*0.6)]

    def kill(self):
        """create particles when sprite die"""
        colors = [(200, 20, 20), (180, 11, 11), (200, 0, 0)]
        for i in range(7):
            vector = pg.Vector2(1, 0).rotate(random.randint(1, 359))
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=random.randint(6, self.rect.width//2.5),
                speed=random.randint(6, 10),
                color=random.choice(colors),
                vector=vector,
                life_size=5,
                speed_rate=-0.3,
                size_rate=-0.5))
        return super().kill()


class Rocket(BaseShell, IAreaShell):
    _speed = 5
    _damage = 120
    _area = pg.Rect(0, 0, 150, 150)

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.GetArea().center = pos

    def draw(self, display):
        # pg.draw.rect(display, (255, 255, 0), self.GetArea())
        # for i in self.rects:
        #     pg.draw.rect(display, (0, 255, 10), i)
        # return super().draw(display)
        pass

    def update(self, *args, **kwargs):
        self.GetArea().center = self.rect.center

        colors = [(190, 192, 194), (164, 165, 166),
                  (206, 206, 214), (129, 129, 130)]
        for i in range(2):
            vector = pg.Vector2(0, -1).rotate(random.randint(-20, 20))
            self.particle_group.add(Particle(
                pos=[self.rect.centerx, self.rect.bottom],
                size=random.randint(6, self.rect.width//2.5),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(18, 30),
                size_rate=random.uniform(0.35, 0.6),
                speed_rate=-0.3,
                shape='circle'))
        return super().update(*args, **kwargs)

    def getDamage(self):
        return self._damage

    def kill(self):
        colors = [(255, 0, 0), (255, 140, 0), (255, 90, 0)]
        for i in range(70):
            vector = pg.Vector2(0, -1).rotate(random.randint(-20, 20))
            self.particle_group.add(Particle(
                pos=[random.randint(self.rect.left-self.rect.width//2, self.rect.right+self.rect.width//2), random.randint(
                    self.rect.top - self.rect.height//2, self.rect.bottom + self.rect.height//2)],
                size=random.randint(2, self.rect.width//2),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=vector,
                life_size=random.randint(50, 100),
                size_rate=random.uniform(2, 5),
                speed_rate=-.3,
                shape='circle'))

        return super().kill()


class BurnedShell(BaseShell):
    _speed = 13
    _damage = 15
    PARTICLE_DAMAGE = 7

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)

        self.rects = [pg.Rect(self.rect.x + self.rect.width * 0.375, self.rect.y +
                              self.rect.height * 0.375, self.rect.width*0.25, self.rect.height*0.25)]

    def kill(self):
        colors = [(255, 0, 0), (255, 140, 0), (255, 90, 0)]
        group = self.groups()[0]

        for i in range(random.randint(4, 7)):
            group.add(ParticleShell(
                pos=self.rect.center,
                size=self.rect.width//5,
                speed=random.randint(12, 16),
                color=random.choice(colors),
                vector=pg.Vector2(1, 0).rotate(random.randint(1, 359)),
                damage=self.PARTICLE_DAMAGE,
                life_size=2,
                size_rate=-0.4,
                speed_rate=-0.3,
                shape='square'
            ))
        return super().kill()


# ----------------------------------ENEMT SHELL---------------------------------------------


class RedEnemyShell(RedShell):
    _damage = 2
    _speed = 10

    def __init__(self, images: list, pos, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.movement.changeDirection(update_y=1)

    def damage(self, value):
        return super().kill()


class StarEnemyShell(BaseShell):
    _speed = 3
    _damage = 5

    def __init__(self, images: list, pos, vector: pg.Vector2, particle_group, *groups: AbstractGroup, **kwargs):
        super().__init__(images, pos, particle_group, *groups, **kwargs)
        self.movement.changeDirection(update_y=vector.y)
        self.movement.changeDirection(update_x=vector.x)

    def kill(self):
        colors = ["#8cd7fb", "#71c9f2", "#bfe9fd"]
        for i in range(4):
            self.particle_group.add(Particle(
                pos=self.rect.center,
                size=int(self.rect.width*0.7),
                speed=random.randint(7, 11),
                color=random.choice(colors),
                vector=pg.Vector2(1, 0).rotate(random.randint(1, 359)),
                life_size=random.randint(2, 4),
                size_rate=-random.uniform(0.5, 0.6),
                speed_rate=-0.3,
                shape='square'))

        return super().kill()

    def damage(self, value):
        return self.kill()
