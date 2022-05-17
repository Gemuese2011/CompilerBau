from Exceptions import TypeException


class Array():
    def __init__(self, values):
        if type(values) == list:
            self.values = values
        else:
            raise TypeException("Value " + str(values) + " can't be safed as Array")

    def printArray(self, name):
        print("Array with name: " + str(name))
        for i in range(len(self.values)):
            print("Position " + str(i) + " Value: " + str(self.values[i]))

    def access_element(self, position):
        return self.values[position]

    def print_variable(self, name):
        self.printArray(name)
