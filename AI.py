
from pygame.sprite import Sprite


class WanderingAI:
    def __init__(self, instance=None):
        self.stack = []

        if instance:
            self.Push(instance)

    def Update(self, *args, **kwargs):
        if len(self.stack) > 0:
            self.stack[-1](*args, **kwargs)

    def Get(self):
        return self.stack[-1] if len(self.stack) > 0 else None

    def Push(self, instence):
        self.stack.append(instence)

    def Pop(self):
        if len(self.stack) > 0:
            self.stack.pop(len(self.stack)-1)
