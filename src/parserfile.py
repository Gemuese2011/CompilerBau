'''
Yacc File
'''
from sly import Parser

from Exceptions.NameGivenException import NameGivenException
from Exceptions.NameNotFoundException import NameNotFoundException
from Exceptions.NotWritableException import NotWritableException
from classes import variable
from utils import variables, set_variable
from lexerfile import MyLexer


class MyParser(Parser):
    '''
    Parser of the Compiler
    '''
    tokens = MyLexer.tokens

    def __init__(self, lexer):
        self.lexer = lexer

    @_('declaration_list')
    def expression(self, p):
        '''
        expression : declaration_list
        :param p: readed Data
        '''
        pass

    @_('declaration', 'declaration declaration_list')
    def declaration_list(self, p):
        '''
        declaration_list : declaration |
        declaration_list : declaration declaration_list
        :param p: readed Data
        '''
        pass

    @_('VARIABLE_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE',
       'VARIABLE_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE')
    def declaration(self, p):
        '''
        EXPRESSION : VARIABLE_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE |
        EXPRESSION : VARIABLE_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME in variables:
            raise NameGivenException("Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
        set_variable(p.VARIABLE_NAME, p.VAR_TYPE, p.VARIABLE_VALUE)

    @_('CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE',
       'CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE')
    def declaration(self, p):
        '''
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE |
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME in variables:
            raise NameGivenException("Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")

        set_variable(p.VARIABLE_NAME, p.VAR_TYPE, p.VARIABLE_VALUE, False)

    @_('COMMENT')
    def expression(self, p):
        '''
        expression : COMMENT
        :param p: readed Data
        '''
        pass

    @_('PRINT LPAREN statement RPAREN')
    def expression(self, p):
        '''
        expression : PRINT LPAREN statement RPAREN
        :param p: readed Data
        '''
        pass

    @_('NAMES')
    def statement(self, p):
        '''
        statement : NAMES
        :param p: readed Data
        '''
        print(variables.keys())

    @_('VARIABLES')
    def statement(self, p):
        '''
        statement : VARIABLES
        :param p: readed Data
        '''
        for var in variables:
            variables.get(var).print_variable(var)

    @_('VARIABLE_NAME ASSIGN VARIABLE_VALUE')
    def expression(self, p):
        '''
        EXPRESSION : VARIABLE_NAME ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''

        if p.VARIABLE_NAME not in variables.keys():
            raise NameNotFoundException("Name " + p.VARIABLE_NAME + " not defined")

        if variables[p.VARIABLE_NAME].write:
            variables[p.VARIABLE_NAME].value = p.VARIABLE_VALUE
        else:
            raise NotWritableException("Name \"" + p.VARIABLE_NAME + "\" defined as not writable")


    @_('VARIABLE_NAME EQ VARIABLE_NAME')
    def BOOL_OP(self, p):
        if p.VARIABLE_VALUE0 == p.VARIABLE_VALUE1:
            return True
        else:
            return False

    @_('VARIABLE_NAME GT VARIABLE_NAME')
    def BOOL_OP(self, p):
        if p.VARIABLE_VALUE0 > p.VARIABLE_VALUE1:
            return True
        else:
            return False

    @_('VARIABLE_NAME LT VARIABLE_NAME')
    def BOOL_OP(self, p):
        if p.VARIABLE_VALUE0 < p.VARIABLE_VALUE1:
            return True
        else:
            return False

    @_('VARIABLE_NAME GE VARIABLE_NAME')
    def BOOL_OP(self, p):
        if p.VARIABLE_VALUE0 >= p.VARIABLE_VALUE1:
            return True
        else:
            return False

    @_('VARIABLE_NAME LE VARIABLE_NAME')
    def BOOL_OP(self, p):
        if p.VARIABLE_VALUE0 <= p.VARIABLE_VALUE1:
            return True
        else:
            return False

    @_('BOOL_OP')
    def STATEMENT(self, p):
        pass

    @_('STATEMENT')
    def expression(self, p):
        pass

    @_('IF BOOL_OP THEN STATEMENT')
    def STATEMENT(self, p):
        pass

    @_('IF BOOL_OP THEN STATEMENT ELSE STATEMENT')
    def STATEMENT(self, p):
        pass

    @_('WHILE BOOL_OP DO STATEMENT')
    def STATEMENT(self, p):
        while p.BOOL_OP == True:
            exec(p.statement)

    def error(self, p):
        print("Syntax error in line" + str(p.lineno))
        if not p:
            print("End of File!")
            return

    def error_message(self, line, message):
        print("Error in line " + str(self.lexer.get_line_no()) + ": " + message)
