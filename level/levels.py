import pygame as pg
from logger.logger import get_logger
from sprites.enemy import AsteroidFactory, FirstFlightEnemyFactory, StarEnemyFactory, StrikerEnemyFactory
from changed_group import Groups
from background import BackgroundManager
from timer import Timer
log = get_logger(__name__)


# The base level class is the parent class of all levels. 
# It has a list of factories, a background class, and a mediator. 
# It has a start method that creates a background and a spawn method that creates objects. 
# It has a close method that closes the level. 
# It has a restart method that restarts the level. 
# It has a update method that updates the level. 
# It has a chackDone method that checks if the level is done. 
# It has a Win method that checks if the level is won. 
# It has a property that returns the level's description. 
# It has a property that returns if the level is won. 
# It has a __str__ method that returns the level's name
class BaseLevel:
    factories = []
    mediator = None
    background_class = None

    def __init__(self, mediator, grops: Groups):
        self.aplication = mediator
        self.grops = grops
        self.__isWin = False

    def start(self):
        self.background = self.background_class(
            self.aplication.display_size, self.grops.Background)

    def close(self):
        pass

    def spawn(self):
        pass

    def countObjects(self):
        counter = 0
        for ft in self.factories:
            counter += ft.count()
        return counter

    def restart(self):
        self.__init__(self.aplication, self.grops)

    def update(self, *args, **kwargs):
        self.background.update()
        self.chackDone(*args, **kwargs)

    def chackDone(self, *args, **kwargs):
        pass

    @property
    def discription(self):
        return ''

    @property
    def isWin(self):
        return self.__isWin

    def Win(self):
        self.__isWin = True
        return self.__isWin

    def __str__(self):
        return self.__class__.__name__


# The Level1 class is a subclass of BaseLevel. 
# It has a list of factories, which are used to create objects. 
# The factories are created in the start method. 
# The update method checks if it's time to create an object from the factory. 
# The chackDone method checks if the level is done. 
# The Win method is called when the level is done.
class Level1(BaseLevel):
    factories = []
    background_class = BackgroundManager

    def __init__(self, mediator, grops: Groups):
        super().__init__(mediator, grops)
        self.spawn_rates = {
            'asteroid': 3000,
            'flightEnemy': 8000
        }
        self.last_spawn_time = {i: 0 for i in self.spawn_rates.keys()}

    @property
    def discription(self):
        return 'Simple level'

    def start(self):
        self.asteroidFactory = AsteroidFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup)
        self.firstFlightFactory = FirstFlightEnemyFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup, particle_group=self.grops.Particles)
        self.starEnemyFactory = StarEnemyFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup, particle_group=self.grops.Particles)

        self.factories.append(self.asteroidFactory)
        self.factories.append(self.firstFlightFactory)
        self.factories.append(self.starEnemyFactory)

        self.last_spawn_time['flightEnemy'] = -5000

        return super().start()

    def update(self, *args, **kwargs):
        now = Timer.get_ticks()

        if now - self.last_spawn_time['asteroid'] > self.spawn_rates['asteroid']:
            self.last_spawn_time['asteroid'] = now
            self.asteroidFactory.createObject()

        if now - self.last_spawn_time['flightEnemy'] > self.spawn_rates['flightEnemy']:
            self.last_spawn_time['flightEnemy'] = now
            if self.firstFlightFactory.count() < 3:
                self.firstFlightFactory.createObject()

        if now//1000 > 10 and self.firstFlightFactory.information.killed >= 3:
            if self.starEnemyFactory.information.killed < 5:
                if self.starEnemyFactory.count() < 1:
                    self.starEnemyFactory.createObject()

        return super().update(*args, **kwargs)

    def chackDone(self, *args, **kwargs):
        if self.firstFlightFactory.information.killed >= 5 and self.starEnemyFactory.information.killed >= 2:
            self.Win()
        return super().chackDone(*args, **kwargs)


class AsteroidWaves(BaseLevel):
    factories = []
    background_class = BackgroundManager

    def __init__(self, mediator, grops: Groups):
        super().__init__(mediator, grops)
        self.spawn_rates = {
            'asteroid': 300,
        }
        self.last_spawn_time = {i: 0 for i in self.spawn_rates.keys()}

    @property
    def discription(self):
        return 'You need to kill more than 200 asteroids'

    def start(self):
        self.asteroidFactory = AsteroidFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup)
        self.factories.append(self.asteroidFactory)

        return super().start()

    def update(self, *args, **kwargs):
        now = Timer.get_ticks()
        if now - self.last_spawn_time['asteroid'] > self.spawn_rates['asteroid']:
            self.last_spawn_time['asteroid'] = now
            self.asteroidFactory.createObject()

        return super().update(*args, **kwargs)

    def chackDone(self, *args, **kwargs):
        if self.asteroidFactory.information.killed > 200:
            self.__isWin
        return super().chackDone(*args, **kwargs)


class StrikerField(BaseLevel):
    factories = []
    background_class = BackgroundManager

    def start(self):
        self.strikerFactory = StrikerEnemyFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup)
        self.factories.append(self.strikerFactory)
        return super().start()

    def update(self, *args, **kwargs):
        now = Timer.get_ticks()
        if self.strikerFactory.count() < 1:
            self.strikerFactory.createObject()

        return super().update(*args, **kwargs)
