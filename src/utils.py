from Exceptions.TypeException import TypeException
from classes import boolean, charClass, floatClass, integer, string
variables = {}

def set_variable(name, var_type, value, write=True):
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

    try:
        value = switch_type.get(var_type)(value)
    except:
        raise TypeException("Value " + value + " is not Type " + var_type)

    if type(value) is switch_type.get(var_type):
        variables[name] = switch_classes.get(var_type)(value, write)

    else:
        raise TypeException("Value " + value + " is not Type " + var_type)
