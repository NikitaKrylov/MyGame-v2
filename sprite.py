import pygame as pg
from pygame.sprite import AbstractGroup, Group, groupcollide


class CustomGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def draw(self, surface, *args, **kwargs):
        sprites = self.sprites()

        for sprite in sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(surface, *args, **kwargs)


class Groups:
    def __init__(self):
        self.enemyGroup = CustomGroup()
        self.playerShell = Group()
        self.objectsGroup = Group()
        self.Particles = Group()
        self._groups = [self.enemyGroup, self.playerShell,
                        self.objectsGroup, self.Particles]

    def collide(self, player):
        # enemy and shell collision
        for enemy in self.enemyGroup:
            shell = spritecollide(enemy, self.playerShell)
            if shell:
                enemy.damage(shell.getDamage())

        # player and enemy collision
        res = spritecollide(player, self.enemyGroup)
        if res:
            player.damage(res.getDamage())

    def update(self, *args, **kwargs):
        for _group in self._groups:
            _group.update(*args, **kwargs)

    def draw(self, display, *args, **kwargs):
        for _group in self._groups:
            _group.draw(display)

    def count(self):
        _counter = 0
        for _group in self._groups:
            _counter += len(_group.sprites())
        return _counter


def twospritecollide(spritea, spriteb, killa=False, killb=False):
    for rects1 in spritea.rects:
        collide_rect_func = rects1.colliderect
        for rects2 in spriteb.rects:
            if collide_rect_func(rects2):
                if killa:
                    spritea.kill()
                if killb:
                    spriteb.kill()

                return spriteb


def spritecollide(sprite, group, killa=False, killb=False):
    """find Sprites in a Group that intersect another Sprite"""

    for group_sprite in group:
        if twospritecollide(group_sprite, sprite):
            if killa:
                sprite.kill()
            if killb:
                group_sprite.kill()

            return group_sprite
