from typing import List
import pygame as pg
from pygame.sprite import Group, Sprite, AbstractGroup
from sprites.enemy import AbstaractFlightEnemy, IInertial
from sprites.shell import IAreaShell


class CustomGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def draw(self, surface, *args, **kwargs):
        sprites = self.sprites()

        for sprite in sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(surface, *args, **kwargs)

# The Static Groups class is a container for all the groups in the game.


class Groups:
    enemyGroup = CustomGroup()
    playerShell = CustomGroup()
    objectsGroup = Group()
    Particles = CustomGroup()
    Background = CustomGroup()
    Interface = CustomGroup()
    _groups: List[AbstractGroup] = [
        Background,
        enemyGroup,
        playerShell,
        objectsGroup,
        Particles,
        Interface]

    @staticmethod
    def GetGroups():
        return Groups._groups

    @staticmethod
    def collide(player):
        # enemy and shell collision
        for enemy in Groups.enemyGroup:
            for shell in Groups.playerShell.sprites():
                if isinstance(shell, IAreaShell):
                    # collision between shell and group of enemy
                    if spritecollide(shell, Groups.enemyGroup):
                        collide_list = shell.CollideGroup(Groups.enemyGroup)
                        [sprite.damage(shell.getDamage())
                         for sprite in collide_list]
                        shell.kill()

                else:
                    # collision between a shel and an enemy
                    sprite = twospritecollide(shell, enemy)  # -> enemy
                    if sprite is not None:
                        sprite.damage(shell.getDamage())

        # collision between player and enemy
        enemy_sprite = spritecollide(player, Groups.enemyGroup)

        if enemy_sprite:
            if not player.isGodMod:
                player.damage(enemy_sprite.getDamage())
                if isinstance(enemy_sprite, IInertial):
                    player.ReactToDamage(
                        direction=pg.Vector2(0, 1),
                        force=enemy_sprite.rect.height*1.1,
                        enemy_rect=enemy_sprite.rect)

    @staticmethod
    def update(*args, **kwargs):
        for _group in Groups.GetGroups():
            _group.update(*args, **kwargs)
        # print(self.Background)

    @staticmethod
    def draw(display, *args, **kwargs):
        for _group in Groups.GetGroups():
            _group.draw(display)

    @staticmethod
    def count():
        _counter = 0
        for _group in Groups.GetGroups():
            _counter += len(_group.sprites())
        return _counter

    @staticmethod
    def restart():
        for group in Groups.GetGroups():
            group.empty()


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
