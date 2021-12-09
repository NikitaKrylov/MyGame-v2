from lavels import Level, Level1
from player import Player
from control import ControlImplementation, JoystickControle, KeyboardControle, BaseController
# from display import Display
import pygame as pg
import sys
from pygame import Surface


class Game:  # Mediator
    controller = None
    controleRealization = {
        KeyboardControle.name: KeyboardControle,
        JoystickControle.name: JoystickControle
    }

    def __init__(self, level: Level, controllerType: str = 'keyboard', *args, **kwargs):
        pg.init()

        self.display = pg.display.set_mode((900, 1200))
        self.clock = pg.time.Clock()

        if controllerType:
            self.controller = self.controleRealization[controllerType](
                ControlImplementation(*args, **kwargs))

        self.player = Player(
            (self.display.get_width(), self.display.get_height()), self)
        self.level = level(self)

    def close(self):
        self.layer.close()

    def restart(self):
        pass

    def setController(self, controllerType, *args, **kwargs):
        if controllerType in self.controleRealization:
            if not self.controller:
                self.controller = self.controleRealization[controllerType](
                    ControlImplementation(*args, **kwargs))

            else:
                _controleImpl = self.controller.getImpl()
                self.controller = self.controleRealization[controllerType](
                    _controleImpl)

        return f'Controller was removed to {self.controller.type()}'

    def eventListener(self):
        pass

    def playerMovementControle(self, player: Player, controller: BaseController, *args, **kwargs):
        _pressed_keys = pg.key.get_pressed()
        controller.changePlayerDirection(player, _pressed_keys)

    def run(self, *args, **kwargs):
        while True:
            self.playerMovementControle(
                self.player, self.controller)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.controller.executeWeapon(self.player, event)

                # if event.type == pg.JOYBUTTONDOWN:
                #     if event.button == 2:
                #         self.controller.

            self.display.fill([153, 230, 170])
            self.player.update()
            self.player.draw(self.display)

            pg.display.update()
            self.clock.tick(60)

    def showMenu(self):
        pass

    def showDiedMenu(self):
        pass

    def showWinMenu(self):
        pass

    def showSettings(self):
        pass


class GameMediator:
    pass


class GameAplication:
    game = GameMediator

    def __init__(self):
        pass


if __name__ == '__main__':
    game = Game(level=Level1, controllerType='joystick')
    game.run()


"""
1. Нужно использовать паттерн комманда, чтобы вызывать меню игры и 
выполянять другие действия. 
2. Использовать паттерн Bridge, чтобы сделать управление через несколько
вариаций устройств
2.2 Вынести максимально возможное количество функций программы в абстрактные 
классы и функции
2.3 Конкретизировать классы только способом взаимодействия с этими функциями
"""
