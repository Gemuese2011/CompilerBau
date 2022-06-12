'''
Yacc File
'''
from sly import Parser

from Exceptions.NameGivenException import NameGivenException
from Exceptions.NameNotFoundException import NameNotFoundException
from Exceptions.NotWritableException import NotWritableException
from classes import variable
from utils import variables, set_variable, cast_value, set_array
from lexerfile import MyLexer


class MyParser(Parser):
    '''
    Parser of the Compiler
    '''
    tokens = MyLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

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
        try:
            if type(p.statement) == str:
                raise TypeError
            for element in p.statement:
                if type(element) == tuple:
                    element[1].print_variable(element[0])
                else:
                    print(element)
        except:
            print(p.statement)

    @_('NAMES')
    def statement(self, p):
        '''
        statement : NAMES
        :param p: readed Data
        '''
        return variables.keys()

    @_('VARIABLES')
    def statement(self, p):
        '''
        statement : VARIABLES
        :param p: readed Data
        '''
        return variables.items()

    @_('VARIABLE_NAME')
    def statement(self, p):
        '''
        statement : VARIABLES
        :param p: readed Data
        '''
        return variables.get(p.VARIABLE_NAME).value

    @_('VARIABLE_NAME L_SQUARE_BRACKETS VARIABLE_VALUE R_SQUARE_BRACKETS')
    def statement(self, p):
        '''
        statement : VARIABLES
        :param p: readed Data
        '''
        return variables.get(p.VARIABLE_NAME).values[int(p.VARIABLE_VALUE)]


    @_('expr')
    def statement(self, p):
        return p.expr

    @_('VARIABLE_NAME ASSIGN expr')
    def expression(self, p):
        '''
        EXPRESSION : VARIABLE_NAME ASSIGN VARIABLE_VALUE
        :param p: readed tokens with values
        '''

        if p.VARIABLE_NAME not in variables.keys():
            raise NameNotFoundException("Name " + p.VARIABLE_NAME + " not defined")

        if variables[p.VARIABLE_NAME].write:
            variables[p.VARIABLE_NAME].value = p.expr
        else:
            raise NotWritableException("Name \"" + p.VARIABLE_NAME + "\" defined as not writable")

    @_('VARIABLE_NAME EQ VARIABLE_NAME')
    def bool_op(self, p):
        return p.expr0 == p.expr1

    @_('VARIABLE_NAME GT VARIABLE_NAME')
    def bool_op(self, p):
        return p.expr0 > p.expr1

    @_('VARIABLE_NAME LT VARIABLE_NAME')
    def bool_op(self, p):
        return p.expr0 < p.expr1

    @_('VARIABLE_NAME GE VARIABLE_NAME')
    def bool_op(self, p):
        return p.expr0 >= p.expr1

    @_('VARIABLE_NAME LE VARIABLE_NAME')
    def bool_op(self, p):
        return p.expr0 <= p.expr1

    @_('bool_op')
    def statement(self, p):
        return p.bool_op

    @_('IF bool_op THEN statement')
    def statement(self, p):
        if p.bool_OP:
            return p.statement

    @_('IF bool_op THEN statement ELSE statement')
    def statement(self, p):
        if p.bool_op:
            return p.statement1
        else:
            return p.statement2

    @_('WHILE bool_op DO statement')
    def statement(self, p):
        while p.bool_op:
            p.statement
        return p.statement


    @_('CAST VARIABLE_NAME TO VAR_TYPE')
    def expression(self, p):
        '''
        EXPRESSION : CAST VARIABLE_NAME TO VAR_TYPE
        :param p: readed tokens with values
        '''
        if p.VARIABLE_NAME not in variables.keys():
            raise NameNotFoundException("Name " + p.VARIABLE_NAME + " not defined")

        cast_value(p.VARIABLE_NAME, p.VAR_TYPE)

    @_('VARIABLE_NAME IS ARRAY OF VAR_TYPE WITH L_SQUARE_BRACKETS value_list R_SQUARE_BRACKETS')
    def expression(self, p):
        set_array(p.VARIABLE_NAME, p.VAR_TYPE, p.value_list)

    @_('expr "+" expr')
    def expr(self, p):
        return float(p.expr0) + float(p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return float(p.expr0) - float(p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return float(p.expr0) * float(p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return float(p.expr0) / float(p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return float(-p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('VARIABLE_VALUE')
    def expr(self, p):
        return p.VARIABLE_VALUE


    @_('VARIABLE_VALUE COMMA value_list',
       'VARIABLE_VALUE')
    def value_list(self, p):
        if len(p) > 1:
            p.value_list.insert(0, p.VARIABLE_VALUE)
            return p.value_list
        else:
            return [p.VARIABLE_VALUE]


    def error(self, p):
        print("Syntax error")
        if not p:
            print("End of File!")
            return

