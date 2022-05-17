from classes.variable import Variable


class Float(Variable):
    def __init__(self, value, write=True):
        super().__init__("float", float(value), write)