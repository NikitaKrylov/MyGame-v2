import pygame as pg
from pygame.sprite import DirtySprite
from pygame.transform import threshold
from player import Player
import json
import os


def sign(value):
    return 1 if value > 0 else -1


class ControlImplementation:
    def __init__(self, *args, **kwargs):
        pass

    def quit(self):
        return 'Игра завершена'

    def showMenu(self):
        return 'Меню показано'

    def executeWeapon(self, player):
        return player.executeWeapon()

    def showSettings(self):
        return 'Настройки показаны'

    def changePlayerDirection(self, player: Player, scancode: pg.key.ScancodeWrapper = None, *args, **kwargs):
        pass

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

    def showMenu(self, *args, **kwargs):
        return self.__implementation.showMenu()

    def showSettings(self, *args, **kwargs):
        return self.__implementation.showSettings()

    def setImpl(self, controlIMPL):
        self.__implementation = controlIMPL

    def getImpl(self):
        return self.__implementation

    def executeWeapon(self, player):
        return self.__implementation.executeWeapon(player)

    def changeControl(self, previous: str, new: str):
        pass

    def eventExecute(self, event, *args, **kwargs):
        config = {'esc': 'showMenu'}
        if event in config:
            return getattr(self, config[event])(*args, **kwargs)

    def changePlayerDirection(self, player: Player, scancode: pg.key.ScancodeWrapper = None, *args, **kwargs):
        pass

    def type(self):
        return self.name

    def __str__(self):
        return 'Управляющая логика'


class JoystickControle(BaseController):
    name = 'joystick'
    ball_threshold = 0.25

    def __init__(self, controlIMPL: ControlImplementation, *args, **kwargs):
        super().__init__(controlIMPL, *args, **kwargs)
        self.config = self.config[self.name]
        pg.joystick.init()
        self.joysticks = [pg.joystick.Joystick(
            x) for x in range(pg.joystick.get_count())]
        self.joystick = self.joysticks[0]

    def getAllContrillers(self):
        return self.joysticks

    def changePlayerDirection(self, player: Player, scancode: pg.key.ScancodeWrapper = None, *args, **kwargs):
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
        if self.config['executeWeapon']['button']:
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == self.config['executeWeapon']['button']:
                    return super().executeWeapon(player)


class KeyboardControle(BaseController):
    name = 'keyboard'

    def __init__(self, controlIMPL: ControlImplementation, *args, **kwargs):
        super().__init__(controlIMPL, *args, **kwargs)
        self.config = self.config[self.name]
        print(self.config)

    def changePlayerDirection(self, player: Player, scancode=None, *args, **kwargs):
        if scancode:

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
        if self.config['executeWeapon']['mouse']:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == self.config['executeWeapon']['mouse']:
                    return super().executeWeapon(player)
