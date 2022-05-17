from classes.variable import Variable


class Char(Variable):
    def __init__(self, value, write=True):
        super().__init__("char" , chr(value), write)