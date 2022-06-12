from Exceptions.TypeException import TypeException
from classes import boolean, charClass, floatClass, integer, string
from classes.array import Array
from src.Exceptions.NameNotFoundException import NameNotFoundException
from src.Exceptions.NotWritableException import NotWritableException

variables = {}

EMPTY_VALUE = ""

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


def redefine_variable(param_array):
    variable_name = param_array[0]
    param_array_copy=param_array.copy()
    variable_value = evaluate_bool(param_array_copy[1])
    if variable_name not in variables.keys():
        raise NameNotFoundException("Name " + variable_name + " not defined")

    if variables[variable_name].write:
        variables[variable_name].value = variable_value
    else:
        raise NotWritableException("Name \"" + variable_name + "\" defined as not writable")


def print_value(value):
    print(value[0])


code_fragment_switch = {
    "print": print_value,
    "redefine": redefine_variable
}


def run_code_fragment(fragment):
    for code in fragment:
        code_fragment_switch.get(code[0])(code[1])


def divide(num1, num2):
    return num1 / num2


def multiply(num1, num2):
    return num1 * num2


def add(num1, num2):
    return num1 + num2


def less_than(num1, num2):
    return num1 < num2


def less_equal(num1, num2):
    return num1 <= num2


def greater_equal(num1, num2):
    return num1 >= num2


def equals(num1, num2):
    return num1 == num2


def subtract(num1, num2):
    return num1 - num2


def greater_than(num1, num2):
    return num1 > num2


def not_equals(num1, num2):
    return num1 != num2


def get_variable_value(variable_name, empty_value):
    return variables[variable_name].value


operator_switch = {
    "/": divide,
    "*": multiply,
    "-": subtract,
    "+": add,
    "le": less_equal,
    "ge": greater_equal,
    "lt": less_than,
    "gt": greater_than,
    "neq": not_equals,
    "eq": equals,
    "var": get_variable_value
}


def evaluate_bool(bool_op):
    try:
        if type(bool_op[1][1]) == list:
            bool_op[1][1] = evaluate_bool(bool_op[1][1])
        if type(bool_op[1][2]) == list:
            bool_op[1][2] = evaluate_bool(bool_op[1][2])
        return operator_switch.get(bool_op[1][0])(bool_op[1][1], bool_op[1][2])
    except:
        return bool_op[0]
