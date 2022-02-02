
import pygame as pg
import pygame.gfxdraw

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
                MEDIA + '\\font\\karmasuture.ttf', int(self.rect.height*0.95))
            self.values = [self.font.render(
                str(i), False, self.color) for i in range(self.MAX_HP//2)]

            for i in range(self.MAX_HP//2, self.MAX_HP+1):
                self.values.append(self.font.render(
                    str(i), False, (255, 255, 255)))

    def draw(self, display, *args, **kwargs):
        self.rect.width = (self.HP / self.MAX_HP) * self.rectMAX.width
        if self.background_color:
            pg.draw.rect(display, self.background_color,
                         self.rectMAX, **kwargs)
        pg.draw.rect(display, self.color, self.rect, **kwargs)
        if self.draw_text:
            display.blit(self.values[self.HP], (self.rectMAX.centerx,
                         self.rectMAX.centery-self.values[self.HP].get_height()//2-1))

    def updateHP(self, hp):
        self.HP = hp

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rectMAX.x = x
        self.rectMAX.y = y


class ToolbarCell:
    def __init__(self, images: list, isSelected=False, isUltimate=False,  **pos):
        self.images = images

        if not isUltimate:
            self.images = [pg.transform.scale(image, (int(image.get_width(
            )*0.65), int(image.get_height()*0.65))) for image in self.images]

        self.image = self.images[0]
        self.rect = self.image.get_rect(**pos)
        self.isSelected = isSelected
        self.isUltimate = isUltimate

    def draw(self, display, label: pg.Surface = None):
        display.blit(self.image, self.rect)

        if label != None:
            display.blit(label, label.get_rect(center=self.rect.center))

    def update(self, *args, **kwargs):
        if self.isSelected:
            self.image = self.images[1]
        else:
            self.image = self.images[0]


class Toolbar:
    def __init__(self, display_size, player_equipment):
        self.display_size = display_size
        self.equipment = player_equipment

        images = [pg.image.load(
            IMAGES + f'\menu\\toolbar_section_{i}.png').convert_alpha() for i in range(1, 5)]

        self.cells = [ToolbarCell(images=images[:2], center=[0, self.display_size[1]*.95])
                      for i in range(self.equipment.countWeapons())]
        self.special_cell = ToolbarCell(
            images=images[-2:], bottomright=[0, self.cells[0].rect.bottom], isUltimate=True)

        margin = self.cells[0].rect.width // 2
        self.special_cell.rect.right = display_size[0] - margin*2
        last_pos = self.special_cell.rect.left - margin
        for cell in self.cells:
            cell.rect.right = last_pos
            last_pos -= cell.rect.width + margin
        self.cells.reverse()

    def draw(self, display):
        for i in range(len(self.cells)):
            self.cells[i].draw(display, label=self.equipment._weapon_equipment[i].label_image)

        self.special_cell.draw(
            display, label=self.equipment._ultimate.label_image)

    def update(self, *args, **kwargs):
        self.special_cell.update()

        if self.equipment.isUltimateSelected:
            self.special_cell.isSelected = True
            for cell in self.cells:
                cell.isSelected = False
                cell.update()
            return
        else:
            self.special_cell.isSelected = False

        for i in range(len(self.cells)):
            if self.equipment.weaponIndex == i:
                self.cells[i].isSelected = True
            else:
                self.cells[i].isSelected = False

            self.cells[i].update(*args, **kwargs)
