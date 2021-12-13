import pygame as pg


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


class BurstAnimator(Animator):
    pass
