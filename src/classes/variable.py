class Variable:
    def __init__(self, datatype, value, write=True):
        self.datatype = datatype
        self.value = value
        self.write = write

    def print_variable(self, name):
        if self.write:
            print("Variablename: " + name + " Type: " + str(self.datatype) + " Value: " + str(self.value))
            return
        else:
            print("Constantname: " + name + " Type: " + str(self.datatype) + " Value: " + str(self.value))
