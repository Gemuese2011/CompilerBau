from classes.variable import Variable


class Bool(Variable):
    def __init__(self, value, write=True):
        super().__init__("bool", value, write)