from enemy import FirstEnemyFactory, SecondEnemyFactory, ThirdEnemyFactory


class Level:
    name = 'AbstractLayer'
    factories = []
    mediator = None

    def __init__(self, mediator):
        self.mediator = mediator

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

    def update(self):
        for ft in self.factories:
            ft.update()

    def __str__(self):
        return self.name


class Level1(Level):
    name = 'Layer1'
    factories = []

    def start(self):
        self.factory2 = SecondEnemyFactory()
        self.factory3 = ThirdEnemyFactory()
        self.factories = [self.factory2, self.factory3]
        return super().start()

    def spawn(self):
        [self.factory2.createEnemy() for i in range(10)]
        [self.factory3.createEnemy() for i in range(4)]
        return super().spawn()
