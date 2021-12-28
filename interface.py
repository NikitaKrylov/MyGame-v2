import pygame as pg
from settings import IMAGES, MEDIA


class HealthBar:
    def __init__(self, pos, XP, MAXXP, size, color, *args, **kwargs):
        self.color = color
        self.HP = XP
        self.MAX_HP = MAXXP
        self.width, self.height = size
        self.rectMAX = pg.Rect(pos[0], pos[1], self.width, self.height)
        self.rect = self.rectMAX.copy()
        self.background_color = kwargs.get(
            'background') if kwargs.get('background') else None
        self.draw_text = False

        if kwargs.get('draw_text') == True:
            self.draw_text = True
            self.font = pg.font.Font(
                MEDIA + '\\font\\karmafuture.ttf', int(self.rect.height*0.95))
            self.values = [self.font.render(
                str(i), False, (255, 255, 255)) for i in range(self.MAX_HP+1)]
            

    def draw(self, display, *args, **kwargs):
        self.rect.width = (self.HP / self.MAX_HP) * self.rectMAX.width
        if self.background_color:
            pg.draw.rect(display, self.background_color,
                         self.rectMAX, **kwargs)
        pg.draw.rect(display, self.color, self.rect, **kwargs)
        if self.draw_text:
            display.blit(self.values[self.HP], (self.rectMAX.centerx,
                         self.rectMAX.centery-self.values[self.HP].get_height()//2-3))

    def updateHP(self, hp):
        self.HP = hp

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rectMAX.x = x
        self.rectMAX.y = y


class ToolbarCell:
    def __init__(self, isSelected=False, isUltimate=False, **pos):
        self.images = [pg.image.load(
            IMAGES + f'\menu\\toolbar_section_{i}.png').convert_alpha() for i in range(1, 3)]
        self.images = [pg.transform.scale(image, (int(image.get_width(
        )*0.65), int(image.get_height()*0.65))) for image in self.images]
        self.images.append(pg.image.load(
            IMAGES + '\menu\\toolbar_section_3.png').convert_alpha())
        self.rect = self.images[0].get_rect(**pos)
        self.isSelected = isSelected
        self.isUltimate = isUltimate

    def draw(self, display):
        if self.isSelected:
            display.blit(self.images[0], self.rect)
        elif self.isUltimate:
            display.blit(self.images[2], self.rect)
        else:
            display.blit(self.images[1], self.rect)


class Toolbar:
    def __init__(self, display_size, player_equipment):
        self.display_size = display_size
        self.equipment = player_equipment
        self.cells = [ToolbarCell(center=[0, self.display_size[1]*.95])
                      for i in range(self.equipment.countWeapons())]
        self.special_cell = ToolbarCell(
            bottomright=[0, self.display_size[1]*.95], isUltimate=True)
        # self.cells.append(ToolbarCell(
        #     bottomright=[0, self.display_size[1]*.95], isUltimate=True))

        margin = self.cells[0].rect.width // 2

        self.special_cell.rect.right = display_size[0] - margin*2
        last_pos = self.special_cell.rect.left - margin
        for cell in self.cells:
            cell.rect.right = last_pos
            last_pos -= cell.rect.width + margin
        self.cells.reverse()

    def draw(self, display):
        for cell in self.cells:
            cell.draw(display)

        self.special_cell.draw(display)

    def update(self, *args, **kwargs):
        for i in range(len(self.cells)):
            if self.equipment.weaponIndex == i:
                self.cells[i].isSelected = True
            else:
                self.cells[i].isSelected = False
