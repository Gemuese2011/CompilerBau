'''
Parser File
'''
from sly import Parser
from classes import variable
from utils import variables
from lexerfile import MyLexer


class MyParser(Parser):
    '''
    Parser of the Compiler
    '''
    tokens = MyLexer.tokens

    def __init__(self):
        pass

    @_('VARIABLE_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE',
       'VARIABLE_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE')
    def expression(self, p):
        '''
        EXPRESSION : VARIABLE_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE |
        EXPRESSION : VARIABLE_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME in variables:
            self.error_message(p.lineno,"Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
            return
        variables[p.VARIABLE_NAME] = variable.Variable(p.VAR_TYPE, p.VARIABLE_VALUE)

    @_('CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE',
       'CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE')
    def expression(self, p):
        '''
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE |
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME in variables:
            self.error_message(p.lineno, "Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
            return

        variables[p.VARIABLE_NAME] = variable.Variable(p.VAR_TYPE, p.VARIABLE_VALUE, False)

    @_('PRINT LPAREN VARIABLES RPAREN')
    def expression(self, p):
        '''
        EXPRESSION : PRINT LPAREN VARIABLES RPAREN
        :param p: readed tokens with values
        '''
        for var in variables:
            variables.get(var).print_variable(var)

    @_('PRINT LPAREN NAMES RPAREN')
    def expression(self, p):
        '''
        EXPRESSION : PRINT LPAREN NAMES RPAREN
        :param p: readed tokens with values
        '''
        print(variables.keys())

    def error(self, p):
        print("Syntax error at: " + p.value)
        if not p:
            print("End of File!")
            return

    @_('VARIABLE_NAME ASSIGN VARIABLE_VALUE')
    def expression(self, p):
        '''
        EXPRESSION : VARIABLE_NAME ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        try:
            if variables[p.VARIABLE_NAME].write:
                variables[p.VARIABLE_NAME].value = p.VARIABLE_VALUE
            else:
                self.error_message(p.lineno,"Name \"" + p.VARIABLE_NAME + "\" defined as not writable")
        except:
            self.error_message(p.lineno,"Name " + p.VARIABLE_NAME + " not defined")

    def error_message(self, lineno, message):
        print("Error in line " + str(lineno) + ": " + message)