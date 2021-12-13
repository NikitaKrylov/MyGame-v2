import pygame
from pygame.sprite import Sprite, AbstractGroup
from animation import Animator


class BaseShell(Sprite):
    isPlayer: bool = None
    animation = Animator

    def __init__(self, images: list,  pos, isPlayer, *groups: AbstractGroup):
        super().__init__(*groups)
        self.animation = self.animation()
        self.DAMAGE = 10
        self.speed = -25
        self.isPlayer = isPlayer
        self.images = images
        self.image = images[0]
        """Изображение, которое должно рисоваться в данный момент,
        должно быть названо image для нормально работы группы
        """
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        # self.animation.update(now=kwargs['now'], rate=80, frame_len=len(self.images), repeat=True)

        if self.rect.bottom < -self.rect.bottom:
            self.kill()

        return super().update(*args, **kwargs)

    def damage(self):
        return self.DAMAGE


class FirstShell(BaseShell):
    def __init__(self, images: list, pos, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.DAMAGE = 10
        self.speed = -25


class SecondShell(BaseShell):
    def __init__(self, images: list, pos, *groups: AbstractGroup):
        super().__init__(images, pos, *groups)
        self.DAMAGE = 10
        self.speed = -19
