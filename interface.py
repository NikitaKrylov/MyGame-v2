import pygame as pg


class HealthBar:
    def __init__(self, pos, XP, MAXXP, width, height, color, *args, **kwargs):
        self.color = color
        self.HP = XP
        self.MAX_HP = MAXXP
        self.width, self.height = width, height
        self.rectMAX = pg.Rect(pos[0], pos[1], self.width, self.height)
        self.rect = self.rectMAX.copy()
        self.background_color = kwargs.get(
            'background') if kwargs.get('background') else None

    def draw(self, display):
        self.rect.width = (self.HP / self.MAX_HP) * self.rectMAX.width
        if self.background_color:
            pg.draw.rect(display, (119, 119, 119), self.rectMAX)
        pg.draw.rect(display, self.color, self.rect)

    def damage(self, value):
        self.HP -= value

    def update(self):
        pass
