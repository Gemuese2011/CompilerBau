from Exceptions.TypeException import TypeException
from classes import boolean, charClass, floatClass, integer, string
from classes.array import Array

variables = {}

switch_classes = {
    "bool": boolean.Bool,
    "int": integer.Integer,
    "String": string.String,
    "float": floatClass.Float,
    "char": charClass.Char
}

switch_type = {
    "bool": bool,
    "int": int,
    "String": str,
    "float": float,
    "char": chr
}


def set_variable(name, var_type, value, write=True):
    try:
        value = switch_type.get(var_type)(value)
    except:
        raise TypeException("Value " + value + " is not Type " + var_type)

    if type(value) is switch_type.get(var_type):
        variables[name] = switch_classes.get(var_type)(value, write)

    else:
        raise TypeException("Value " + value + " is not Type " + var_type)


def cast_value(name, var_type):

    try:
        variables[name] = switch_classes.get(var_type)(variables[name].value, variables[name].write)
    except:
        raise TypeException("Value " + variables[name].value + " can't be casted to " + var_type)


def set_array(name, var_type, value):
    for i in range(len(value)):
        value[i] = switch_type.get(var_type)(value[i])
    variables[name] = Array(value)