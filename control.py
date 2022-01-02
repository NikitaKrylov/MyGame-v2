import pygame as pg
from pygame.display import update
from pygame.sprite import DirtySprite
from pygame.transform import threshold
from player import Player
import json
import os


def sign(value):
    return 1 if value > 0 else -1


class ControlImplementation:
    def __init__(self, mediator, *args, **kwargs):
        self.aplication = mediator

    def quit(self):
        return 'Игра завершена'

    def showMenu(self):
        """Show and close menu"""
        return self.aplication.showMenu()

    def executeWeapon(self, player):
        return player.executeWeapon()

    def changeWeapon(self, player, update=None, value=None):
        return player.changeWeapon(value=value, update=update)

    def showSettings(self):
        return 'Настройки показаны'

    def changePlayerDirection(self, player: Player, *args, **kwargs):
        pass

    def menuExecute(self, *args, **kwargs):
        self.aplication._actingStrategy.menu.execute(*args, **kwargs)

    def menuUpdate(self, *args, **kwargs):
        return self.aplication._actingStrategy.menu.update(*args, **kwargs)

    def __str__(self):
        return 'Базовая реализация функций управления'


class BaseController:  # Interface
    __implementation: ControlImplementation = None
    config = None
    name = 'base_controller'

    def __init__(self, controlIMPL: ControlImplementation, *args, **kwargs):
        self.__implementation = controlIMPL
        self.config = self.load_config(os.getcwd()+'\control_config.json')

    def load_config(self, path=None):
        with open(path, 'r') as file:
            _config = json.load(file)

        return _config

    def quit(self, *args, **kwargs):
        return self.__implementation.quit()

    def showMenu(self, event, *args, **kwargs):
        """call aplication showMenu"""
        return self.__implementation.showMenu()

    def showSettings(self, *args, **kwargs):
        return self.__implementation.showSettings()

    def setImpl(self, controlIMPL):
        self.__implementation = controlIMPL

    def getImpl(self):
        return self.__implementation

    def executeWeapon(self, player):
        """call player execiteWeapon"""
        return self.__implementation.executeWeapon(player)

    def changeControl(self, previous: str, new: str):
        pass

    def eventExecute(self, event, *args, **kwargs):
        config = {'esc': 'showMenu'}
        if event in config:
            return getattr(self, config[event])(*args, **kwargs)

    def changePlayerDirection(self, player: Player, *args, **kwargs):
        pass

    def changeWeapon(self, player, update=None, value=None):
        self.__implementation.changeWeapon(player, update, value)

    def menuExecute(self, event, *args, **kwargs):
        self.__implementation.menuExecute(*args, **kwargs)

    def menuUpdate(self, event, *args, **kwargs):
        self.__implementation.menuUpdate(*args, **kwargs)

    def type(self):
        return self.name

    def __str__(self):
        return 'Управляющая логика'


class JoystickControle(BaseController):
    name = 'joystick'
    ball_threshold = 0.25

    def __init__(self, controlIMPL: ControlImplementation, ball_threshold: float = 0.25, *args, **kwargs):
        super().__init__(controlIMPL, *args, **kwargs)
        self.config = self.config[self.name]
        self.ball_threshold = ball_threshold
        pg.joystick.init()
        self.joysticks = [pg.joystick.Joystick(
            x) for x in range(pg.joystick.get_count())]
        self.joystick = self.joysticks[0]
        self.btnHoverIndex = 0

    def getAllContrillers(self):
        return self.joysticks

    def changePlayerDirection(self, player: Player, *args, **kwargs):
        jx = round(self.joystick.get_axis(0), 2)
        jy = round(self.joystick.get_axis(1), 2)

        """        X AXIS        """
        if abs(jx) < self.ball_threshold:
            player.decreaseAccel(0)
        else:
            player.direction.x = jx
            player.increaseAccel(0)

        """        Y AXIS        """
        if abs(jy) < self.ball_threshold:
            player.decreaseAccel(1)
        else:
            player.direction.y = jy
            player.increaseAccel(1)

    def changeJoysticks(self, value=0):
        self.joysticks = [pg.joystick.Joystick(
            x) for x in range(pg.joystick.get_count())]

        if 0 < value < len(self.joysticks):
            self.joystick = self.joysticks[value]

    def executeWeapon(self, player, event):
        if event.type == pg.JOYBUTTONDOWN:
            if event.button == self.config['executeWeapon']['button']:
                return super().executeWeapon(player)

    def showMenu(self, event, *args, **kwargs):
        if event.type == pg.JOYBUTTONDOWN:
            if event.button in self.config['showMenu']:
                return super().showMenu(event, *args, **kwargs)

    def changeWeapon(self, player, event):
        if event.type == pg.JOYBUTTONDOWN:
            if event.button in [9, 10]:
                _update_value = 0
                if event.button == 9:
                    _update_value = -1
                elif event.button == 10:
                    _update_value = 1

                return super().changeWeapon(player, update=_update_value)

    def menuExecute(self, event, *args, **kwargs):
        if event.type == pg.JOYBUTTONDOWN:
            if event.button == 0:
                return super().menuExecute(event, *args, isController=True, controller=self.btnHoverIndex)

    def menuUpdate(self, event, *args, **kwargs):
        if event.type == pg.JOYBUTTONDOWN:
            if event.button in [11, 12, 13, 14]:
                if event.button in [12, 14]:
                    self.btnHoverIndex += 1
                elif event.button in [11, 13]:
                    if self.btnHoverIndex - 1 < 0:
                        self.btnHoverIndex = 0
                    else:
                        self.btnHoverIndex -= 1
        return super().menuUpdate(event, *args, isController=True, controller=self.btnHoverIndex)


class KeyboardControle(BaseController):
    name = 'keyboard'

    def __init__(self, controlIMPL: ControlImplementation, *args, **kwargs):
        super().__init__(controlIMPL, *args, **kwargs)
        self.config = self.config[self.name]

    def changePlayerDirection(self, player: Player, *args, **kwargs):
        """Update player direction by axis"""
        scancode = pg.key.get_pressed()

        """                    X AXIS               """
        if not (scancode[pg.K_a] or scancode[pg.K_d]):
            # управляет изменением ускоренной скорости
            player.decreaseAccel(0)
        else:
            if scancode[pg.K_a]:
                player.direction.x = -1
            if scancode[pg.K_d]:
                player.direction.x = 1

            # управляет изменением ускоренной скорости
            player.increaseAccel(0)

        """                Y AXIS                   """
        if not (scancode[pg.K_w] or scancode[pg.K_s]):
            # управляет изменением ускоренной скорости
            player.decreaseAccel(1)
        else:
            if scancode[pg.K_w]:
                player.direction.y = -1
            if scancode[pg.K_s]:
                player.direction.y = 1

            # управляет изменением ускоренной скорости
            player.increaseAccel(1)

    def executeWeapon(self, player,  event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == self.config['executeWeapon']['mouse']:
                return super().executeWeapon(player)

    def showMenu(self, event, *args, **kwargs):
        if event.type == pg.KEYDOWN:
            if event.key in self.config['showMenu']:
                return super().showMenu(event, *args, **kwargs)

    def changeWeapon(self, player, event):
        if event.type == pg.KEYDOWN:
            if 49 <= event.key <= 57:
                return super().changeWeapon(player=player, value=int(event.unicode))

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button in [4, 5]:
                _update_value = 0
                if event.button == 4:
                    _update_value = 1
                elif event.button == 5:
                    _update_value = -1

                return super().changeWeapon(player=player, update=_update_value)

    def menuExecute(self, event, *args, **kwargs):
        if event.type == pg.MOUSEBUTTONDOWN:
            return super().menuExecute(event, *args, **kwargs)

    def menuUpdate(self, event, *args, **kwargs):
        return super().menuUpdate(event, *args, **kwargs)
