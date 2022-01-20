import ctypes, sys, pygame as pg
from GUI.menu import ColoredButton, AplicationMenu
from main import Aplication
from pygame.sprite import Group
from changed_group import CustomGroup



class BaseStrategy:
    def __init__(self):
        self.btnGroup = Group()
        
    def draw(self, display, *args, **kwargs):
        self.btnGroup.draw(display)
    
    def update(self, *args, **kwargs):
        pass
    
    def eventListen(self, *args, **kwargs):
        pass



class AplicationGUI:
    __run = True
    _actingStrategy = None

    def __init__(self):
        pg.init()
        pg.font.init()
        user32 = ctypes.windll.user32

        self.window_size = user32.GetSystemMetrics(
            0), user32.GetSystemMetrics(1)
        self.display_size = [int(0.4*self.window_size[0]),
                             int(0.9*self.window_size[1])]
        self.display = pg.display.set_mode(self.display_size)
        self.clock = pg.time.Clock()
        self.menu = AplicationMenu(self, self.display_size)

    def close(self):
        self.__run = False
    

    def update(self, *args, **kwargs):
        self.menu.update(*args, **kwargs)

    def draw(self, display, *args, **kwargs):
        self.menu.draw(display, *args, **kwargs)

    def start(self, *args, **kwargs):
        while self.__run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                    pg.quit()
                    sys.exit()
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    from levels import AsteroidWaves, Level1
                    aplication = Aplication(Level1)
                    # aplication.changeLevel(AsteroidWaves)
                    # aplication.setControllerType('joystick')
                    aplication.start()
                    self.close()

            # self.display.fill("#182629")
            self.update()
            self.draw(self.display)
            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    aplicatio = AplicationGUI()
    aplicatio.start()
