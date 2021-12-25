from pygame import key
from enemy import AsteroidFactory, FirstFlightEnemyFactory


class Level:
    name = 'AbstractLayer'
    factories = []
    mediator = None

    def __init__(self, mediator, shellGroup=None, enemyGroup=None):
        self.aplication = mediator
        self.shellGroup = shellGroup
        self.enemyGroup = enemyGroup

    def start(self):
        return True

    def close(self):
        pass

    def spawn(self):
        pass

    def countObjects(self):
        counter = 0
        for ft in self.factories:
            counter += ft.count()
        return counter

    # def update(self, now):
    #     for factory in self.factories:
    #         factory.update()

    def __str__(self):
        return self.name


class Level1(Level):
    name = 'Layer1'
    factories = []

    def __init__(self, mediator, shellGroup=None, enemyGroup=None):
        super().__init__(mediator, shellGroup=shellGroup, enemyGroup=enemyGroup)
        self.spawn_rates = {
            'asteroid': 2000,
            'flightEnemy': 7000
        }
        self.last_spawn_time = {i: 0 for i in self.spawn_rates.keys()}


    def start(self):
        self.asteroidFactory = AsteroidFactory(
            display_size=self.aplication.display_size, group=self.enemyGroup)
        self.firstFlightFactory = FirstFlightEnemyFactory(
            display_size=self.aplication.display_size, group=self.enemyGroup)

        self.factories.append(self.asteroidFactory)
        self.factories.append(self.firstFlightFactory)

        return super().start()

    def update(self, now):
        if now - self.last_spawn_time['asteroid'] > self.spawn_rates['asteroid']:
            self.last_spawn_time['asteroid'] = now
            self.asteroidFactory.createObject()

        if now - self.last_spawn_time['flightEnemy'] > self.spawn_rates['flightEnemy']:
            self.last_spawn_time['flightEnemy'] = now
            if self.firstFlightFactory.count() < 3:
                self.firstFlightFactory.createObject()
    
