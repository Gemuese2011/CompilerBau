'''
Yacc File
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
            self.error_message(p.lineno, "Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
            return
        variables[p.VARIABLE_NAME] = variable.Variable(p.VAR_TYPE, p.VARIABLE_VALUE)

    @_('CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE',
       'CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE')
    def declaration(self, p):
        '''
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN VARIABLE_VALUE |
        EXPRESSION : CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME in variables:
            self.error_message(p.lineno, "Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
            return

        variables[p.VARIABLE_NAME] = variable.Variable(p.VAR_TYPE, p.VARIABLE_VALUE, False)

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
        try:
            if variables[p.VARIABLE_NAME].write:
                variables[p.VARIABLE_NAME].value = p.VARIABLE_VALUE
            else:
                self.error_message(p.lineno, "Name \"" + p.VARIABLE_NAME + "\" defined as not writable")
        except:
            self.error_message(p.lineno, "Name " + p.VARIABLE_NAME + " not defined")

    def error(self, p):
        print("Syntax error in line" + p.lineno)
        if not p:
            print("End of File!")
            return

    def error_message(self, lineno, message):
        print("Error in line " + str(self.lexer.get_line_no()) + ": " + message)
