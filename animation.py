from math import sin
import pygame as pg
from pygame import sprite


class Animator:
    updatingTime = 0
    frame = 0
    rotationTime = 0
    rot = 0

    def update(self, now: int, rate: int, frames_len: int, repeat: bool = True, finiteFunction=None):
        if now - self.updatingTime > rate:
            self.updatingTime = now

            if self.frame+1 <= frames_len-1:
                self.frame += 1
            elif repeat:
                self.frame = 0
            elif finiteFunction:
                finiteFunction()

    @property
    def getIteration(self):
        return self.frame

    def rotate(self, now, rot_speed, rect, image, image_copy, cooldawn):
        if now - self.rotationTime > cooldawn:
            self.rotationTime = now
            self.rot = (self.rot + rot_speed) % 360
            new_image = pg.transform.rotate(image, self.rot)
            old_center = rect.center
            image_copy = new_image
            rect = image_copy.get_rect()
            rect.center = old_center

        return rect, image_copy

    def changeImages(self):
        pass


class MovementInterface:
    def update(self, rect, rects, update_pos, *args, **kwargs):
        """have to give new coord for rect/rects"""
        _rect, _rects = self.updateRects(
            rect, rects, update_pos, *args, **kwargs)
        return _rect, _rects

    def updateRects(self, rect, rects, update_pos: list, *args, **kwargs):
        x, y = update_pos
        rect.x = x
        rect.y = y

        for _rect in rects:
            _rect.x = x
            _rect.y = y

        return rect, rects

    def __str__(self):
        return self.__class__.__name__


class CoordMovement(MovementInterface):
    def __init__(self, coord_list: list, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StaticMovement(MovementInterface):
    def __init__(self, vector: pg.Vector2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = vector

    def update(self, rect, rects, update_pos=None, *args, **kwargs):
        """dontb give update_pos"""
        return super().update(rect, rects, update_pos, *args, **kwargs)

    def updateRects(self, rect, rects, update_pos: list = None, *args, **kwargs):

        if kwargs['speed']:
            speed = kwargs['speed']
        else:
            speed = 0

        rect.x += self.direction.x * speed 
        rect.y += self.direction.y * speed
        
        for _rect in rects:
            _rect.x += self.direction.x * speed 
            _rect.y += self.direction.y * speed
        
        return (rect, rects)

    def changeDirection(self, mn_x=None, mn_y=None, update_x=None, update_y=None):
        if mn_x:
            self.direction.x *= mn_x
        if mn_y:
            self.direction.y *= mn_y

        if update_x:
            self.direction.x = update_x
        if update_y:
            self.direction.y = update_y



class FunctionMovement(StaticMovement):
    def __init__(self, vector: pg.Vector2, func, *args, **kwargs):
        super().__init__(vector, *args, **kwargs)
        self.func = func #takes only X

    def update(self, rect, rects, *args, **kwargs):
        # kwargs['speed']
        _rect, _rects = self.updateRects(rect, rects, *args, **kwargs)
        return (_rect, _rects)

    def updateRects(self, rect, rects, *args, **kwargs):
        # kwargs['speed']
        rect.x += (kwargs['speed'] * self.direction.x)
        rect.y = self.func(rect.x)
        
        for _rect in rects:
            _rect.x += kwargs['speed'] * self.direction.x
            _rect.y = self.func(rect.x)
            
        return (rect, rects)


class AbstractParticle(sprite.Sprite):
    def __init__(self, pos: list, speed, rate, life_time=None, *groups: sprite.AbstractGroup):
        super().__init__(*groups)
        self.speed = speed
        self.rate = rate
        self.life_time = life_time



class RectParticle(AbstractParticle):
    def __init__(self, pos: list, speed, rate, surface_size: list, life_time=None, *groups: sprite.AbstractGroup):
        super().__init__(pos, speed, rate, life_time=life_time, *groups)
        self.image = pg.Surface(surface_size)
        self.rect = self.image.get_rect(center=pos)
