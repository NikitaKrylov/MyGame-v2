import pygame as pg
from pygame import key
from sprites.enemy import AsteroidFactory, FirstFlightEnemyFactory
from changed_group import Groups
from background import StarsBackground

class Level:
    factories = []
    mediator = None

    def __init__(self, mediator, grops: Groups):
        self.aplication = mediator
        self.grops = grops

    def start(self):
        line = ''.join(['*' for i in range(int(len(self.discription) * 1.2))])
        return print(
            f"""
            {line}    
            {self.discription}
            {line}
            """
        )

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

    def update(self):
        pass

    @property
    def discription(self):
        return ''

    def __str__(self):
        return self.__class__.__name__


class Level1(Level):
    factories = []

    def __init__(self, mediator, grops: Groups):
        super().__init__(mediator, grops)
        self.spawn_rates = {
            'asteroid': 2500,
            'flightEnemy': 7000
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

        self.factories.append(self.asteroidFactory)
        self.factories.append(self.firstFlightFactory)
        
        self.background = StarsBackground(self.aplication, self.aplication.display_size, self.grops.Background)

        return super().start()

    def update(self, now):
        self.background.update()
        
        if now - self.last_spawn_time['asteroid'] > self.spawn_rates['asteroid']:
            self.last_spawn_time['asteroid'] = now
            self.asteroidFactory.createObject()

        if now - self.last_spawn_time['flightEnemy'] > self.spawn_rates['flightEnemy']:
            self.last_spawn_time['flightEnemy'] = now
            if self.firstFlightFactory.count() < 3:
                self.firstFlightFactory.createObject()

        if self.firstFlightFactory.information['killed'] >= 10:
            print('You won')
            self.aplication.close()


class AsteroidWaves(Level):
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
        now = pg.time.get_ticks()
        if now - self.last_spawn_time['asteroid'] > self.spawn_rates['asteroid']:
            self.last_spawn_time['asteroid'] = now
            self.asteroidFactory.createObject()

        if self.asteroidFactory.information['killed'] > 200:
            print('You won')
            self.aplication.close()
