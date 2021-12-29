from pygame import key
from enemy import AsteroidFactory, FirstFlightEnemyFactory
from sprite import Groups


class Level:
    name = 'AbstractLayer'
    factories = []
    mediator = None

    def __init__(self, mediator, grops:Groups):
        self.aplication = mediator
        self.grops = grops

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

    def restart(self):
        self.__init__(self.aplication, self.grops)

    def __str__(self):
        return self.name


class Level1(Level):
    name = 'Layer1'
    factories = []
    
    def __init__(self, mediator, grops: Groups):
        super().__init__(mediator, grops)
        self.spawn_rates = {
            'asteroid': 2000,
            'flightEnemy': 7000
        }
        self.last_spawn_time = {i: 0 for i in self.spawn_rates.keys()}

    def start(self):
        self.asteroidFactory = AsteroidFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup)
        self.firstFlightFactory = FirstFlightEnemyFactory(
            display_size=self.aplication.display_size, group=self.grops.enemyGroup, particle_group=self.grops.Particles)

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
                
        # if self.firstFlightFactory.information['killed'] >= 7:
        #     self.aplication.close()
            
