import pygame as pg
import math
from timer import Timer


class Animator:
    def __init__(self):
        self.updatingTime = 0
        self.frame = 0
        self.rotationTime = 0
        self.rot = 0
        self.__rotVector = pg.Vector2(1, 0)

    def update(self, rate: int, frames_len: int, repeat: bool = True, finiteFunction=None):
        now = Timer.get_ticks()
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

    def rotate(self, rot_speed, rect, image, image_copy, cooldawn):
        now = Timer.get_ticks()
        if now - self.rotationTime > cooldawn:
            self.rotationTime = now
            self.rot = (self.rot + rot_speed) % 360
            new_image = pg.transform.rotate(image, self.rot)
            old_center = rect.center
            image_copy = new_image
            rect = image_copy.get_rect()
            rect.center = old_center

        return rect, image_copy

    @property
    def rotVector(self):
        return self.__rotVector.rotate_rad(math.radians(-self.rot))


class MovementInterface:
    def __init__(self, *args, **kwargs):
        pass

    def update(self, rect, rects, *args, **kwargs):
        """have to give new coord for rect/rects"""
        return (rect, rects)

    def __str__(self):
        return self.__class__.__name__


class StaticMovement(MovementInterface):
    def __init__(self, vector: pg.Vector2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = vector

    def update(self, rect, rects, *args, **kwargs):

        if kwargs['speed']:
            speed = kwargs['speed']
        else:
            speed = 0

        rect.x += self.direction.x * speed
        rect.y += self.direction.y * speed

        for _rect in rects:
            _rect.x += self.direction.x * speed
            _rect.y += self.direction.y * speed

        return super().update(rect, rects, *args, **kwargs)

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
        self.func = func  # takes only X

    def update(self, rect, rects, *args, **kwargs):
        rect.x += kwargs['speed'] * self.direction.x
        rect.y = self.func(rect.x)

        for _rect in rects:
            _rect.x += kwargs['speed'] * self.direction.x
            _rect.y = self.func(rect.x)

        return super().update(rect, rects, *args, **kwargs)


class PointerMovement(StaticMovement):
    def __init__(self, vector: pg.Vector2, point=None, max_coint_amount=3, *args, **kwargs):
        super().__init__(vector, *args, **kwargs)
        self.next_point = None
        self.point = point if point else None
        self.max_coint_amount = max_coint_amount

    def update(self, rect, rects, *args, **kwargs):
        _vector = pg.Vector2(self.point) - pg.Vector2(rect.center)

        if _vector.length() <= kwargs['speed']:
            self.point = self.next_point
            self.next_point = None
            _vector = pg.Vector2(self.point) - pg.Vector2(rect.center)

        _vector.scale_to_length(1)
        self.direction = _vector
        return super().update(rect, rects, *args, **kwargs)
