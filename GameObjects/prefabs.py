import pygame as pg
from pygame.sprite import AbstractGroup, Sprite







class AimingPoint(Sprite):
    """Hover point class used with some ultimates"""

    def __init__(self, image, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(center=pg.mouse.get_pos())
    
    
    def update(self, *args, **kwargs):
        pg.mouse.set_visible(False)
        joystick_hover_point = kwargs.get('joystick_hover_point')
        if joystick_hover_point:
            self.rect.centerx = joystick_hover_point.x
            self.rect.centery = joystick_hover_point.y
        else:
            self.rect.center = pg.mouse.get_pos()
        return super().update(*args, **kwargs)

    def draw(self, display):
        display.blit(self.image, self.rect)


