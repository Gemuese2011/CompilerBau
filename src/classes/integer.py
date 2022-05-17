from classes.variable import Variable


class Integer(Variable):
    def __init__(self, value, write=True):
        super().__init__("int", int(value), write)
