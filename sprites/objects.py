import pygame as pg
from pygame.sprite import Sprite, AbstractGroup



class ObjectInterface(Sprite):
    def __init__(self, images, pos, *groups: AbstractGroup):
        super().__init__(*groups)
        self.images = images
        self.image = self.image[0]
        self.rect = self.image.get_rect(center=pos)
        
    def draw(self, display):
        pass
    
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def execute(self):
        return 



class ObjectFactoryInterface:
    _object = ObjectInterface
    _group = None
    
    def __init__(self):
        self.images = None
    
    def createObject(self):
        pass
    
    @property
    def count(self):
        return 
    
    def kill(self):
        killed = self.count()
        return killed



