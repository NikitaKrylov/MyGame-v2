class NoneInitializeError(Exception):
    def __init__(self, object:str='', *args):
        self.name_object = object
        super().__init__(*args)

    def __str__(self):
        return f'Variable {self.name_object} is None or not initialized'

