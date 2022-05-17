from classes.variable import Variable


class String(Variable):
    def __init__(self, value, write=True):
        super().__init__("String", str(value), write)