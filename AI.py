
class WanderingAI:
    def __init__(self, instance=None):
        self.__stack = []

        if instance:
            self.Push(instance)

    def Update(self, *args, **kwargs):
        if len(self.__stack) > 0:
            self.__stack[-1](*args, **kwargs)

    def Get(self):
        return self.__stack[-1] if len(self.__stack) > 0 else None

    def Push(self, instence):
        self.__stack.append(instence)

    def Pop(self):
        if len(self.__stack) > 0:
            self.__stack.pop(len(self.__stack)-1)
            
    def __repr__(self):
        return '[' + ', '.join(list(map(lambda f: f.__name__, self.__stack))) + ']'

    def __str__(self):
        return self.__repr__()