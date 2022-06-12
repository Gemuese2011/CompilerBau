'''
Yacc File
'''
from copy import deepcopy

from sly import Parser

from Exceptions.NameGivenException import NameGivenException
from Exceptions.NameNotFoundException import NameNotFoundException
from Exceptions.NotWritableException import NotWritableException
from utils import variables, set_variable, cast_value, set_array, run_code_fragment, evaluate_bool, EMPTY_VALUE
from lexerfile import MyLexer


class MyParser(Parser):
    '''
    Parser of the Compiler
    '''
    tokens = MyLexer.tokens
    debugfile = 'parser.out'

    line = 0

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self, lexer):
        self.lexer = lexer

    @_('declaration_list')
    def expression(self, p):
        pass

    @_('')
    def expression(self, p):
        pass

    @_('declaration', 'declaration declaration_list')
    def declaration_list(self, p):
        pass

    @_('VARIABLE_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN variable_value',
       'VARIABLE_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN variable_value')
    def declaration(self, p):
        if p.VARIABLE_NAME in variables:
            raise NameGivenException("Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")
        set_variable(p.VARIABLE_NAME, p.VAR_TYPE, p.variable_value)

    @_('CONSTANTS_PREFIX VARIABLE_NAME IS VAR_TYPE ASSIGN variable_value',
       'CONSTANTS_PREFIX VARIABLE_NAME COLON VAR_TYPE ASSIGN variable_value')
    def declaration(self, p):
        if p.VARIABLE_NAME in variables:
            raise NameGivenException("Constant/Variable \"" + p.VARIABLE_NAME + "\" already defined")

        set_variable(p.VARIABLE_NAME, p.VAR_TYPE, p.variable_value, False)

    @_('COMMENT')
    def expression(self, p):
        pass


    @_('PRINT LPAREN non_while_statement RPAREN')
    def expression(self, p):
        try:
            if type(p.non_while_statement) == str:
                raise TypeError
            for element in p.non_while_statement:
                if type(element) == tuple:
                    element[1].print_variable(element[0])
                else:
                    print(element)
        except:
            print(p.non_while_statement)

    @_('NAMES')
    def statement(self, p):
        return [variables.keys()]

    @_('VARIABLES')
    def statement(self, p):
        return [variables.items()]

    @_('VARIABLE_NAME L_SQUARE_BRACKETS variable_value R_SQUARE_BRACKETS')
    def statement(self, p):
        return [variables.get(p.VARIABLE_NAME).values[int(p.variable_value)]]

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('VARIABLE_NAME ASSIGN expr')
    def expression(self, p):
        if p.VARIABLE_NAME not in variables.keys():
            raise NameNotFoundException("Name " + p.VARIABLE_NAME + " not defined")

        if variables[p.VARIABLE_NAME].write:
            variables[p.VARIABLE_NAME].value = p.expr
        else:
            raise NotWritableException("Name \"" + p.VARIABLE_NAME + "\" defined as not writable")

    @_('expr EQ expr')
    def bool_op(self, p):
        return [p.expr0[0] == p.expr1[0], ["eq", p.expr0, p.expr1]]

    @_('expr NEQ expr')
    def bool_op(self, p):
        return [p.expr0[0] != p.expr1[0], ["neq", p.expr0, p.expr1]]

    @_('expr GT expr')
    def bool_op(self, p):
        return [p.expr0[0] > p.expr1[0], ["gt", p.expr0, p.expr1]]

    @_('expr LT expr')
    def bool_op(self, p):
        return [p.expr0[0] < p.expr1[0], ["lt", p.expr0 , p.expr1] ]

    @_('expr GE expr')
    def bool_op(self, p):
        return [p.expr0[0] >= p.expr1[0], ["ge", p.expr0, p.expr1]]

    @_('expr LE expr')
    def bool_op(self, p):
        return [p.expr0[0] <= p.expr1[0], ["le", p.expr0, p.expr1]]

    @_('bool_op')
    def statement(self, p):
        return p.bool_op

    @_('IF bool_op THEN code_fragment')
    def expression(self, p):
        if p.bool_op:
            run_code_fragment(p.code_fragment)


    @_('IF bool_op THEN code_fragment ELSE code_fragment')
    def expression(self, p):
        if p.bool_op:
            run_code_fragment(p.code_fragment0)
        else:
            run_code_fragment(p.code_fragment1)


    @_('WHILE bool_op DO code_fragment')
    def expression(self, p):
        run_loop = p.bool_op[0]
        while run_loop:
            code = deepcopy(p.code_fragment)
            run_code_fragment(code)
            bool = deepcopy(p.bool_op)
            if evaluate_bool(bool):
                continue
            else:
                break


    @_('CAST VARIABLE_NAME TO VAR_TYPE')
    def expression(self, p):
        if p.VARIABLE_NAME not in variables.keys():
            raise NameNotFoundException("Name " + p.VARIABLE_NAME + " not defined")

        cast_value(p.VARIABLE_NAME, p.VAR_TYPE)

    @_('VARIABLE_NAME IS ARRAY OF VAR_TYPE WITH L_SQUARE_BRACKETS value_list R_SQUARE_BRACKETS')
    def expression(self, p):
        set_array(p.VARIABLE_NAME, p.VAR_TYPE, p.value_list)

    @_('expr "+" expr')
    def expr(self, p):
        return [float(p.expr0[0]) + float(p.expr1[0]), ["+", p.expr0, p.expr1]]

    @_('expr "-" expr')
    def expr(self, p):
        return [float(p.expr0[0]) - float(p.expr1[0]), ["-", p.expr0, p.expr1]]

    @_('expr "*" expr')
    def expr(self, p):
        return [float(p.expr0[0]) * float(p.expr1[0]), ["*", p.expr0, p.expr1]]

    @_('expr "/" expr')
    def expr(self, p):
        return [float(p.expr0[0]) / float(p.expr1[0]), ["/", p.expr0, p.expr1]]

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return [float(-p.expr)]

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('variable_value')
    def expr(self, p):
        return [p.variable_value]

    @_('variable_value COMMA value_list',
       'variable_value')
    def value_list(self, p):
        if len(p) > 1:
            p.value_list.insert(0, p.variable_value)
            return p.value_list
        return [p.variable_value]

    @_('FLOAT_VALUE')
    def variable_value(self, p):
        return float(p.FLOAT_VALUE)

    @_('INTEGER_VALUE')
    def variable_value(self, p):
        return int(p.INTEGER_VALUE)


    @_('STRING_VALUE')
    def variable_value(self, p):
        return str(p.STRING_VALUE).replace("\"", "")

    @_('VARIABLE_NAME')
    def expr(self, p):
        return [variables.get(p.VARIABLE_NAME).value, ["var", p.VARIABLE_NAME, EMPTY_VALUE]]

    @_('statement',
       'code_fragment SEMICOLON statement')
    def code_fragment(self, p):
        if len(p) > 1:
            p.code_fragment.insert(0, p.statement)
            return p.code_fragment
        return [p.statement]

    @_('PRINT LPAREN statement RPAREN')
    def statement(self, p):
        return ["print", p.statement]

    @_('VARIABLE_NAME ASSIGN expr')
    def statement(self, p):
        return ["redefine", [p.VARIABLE_NAME, p.expr]]

    @_('statement')
    def non_while_statement(self, p):
        return p.statement[0]

    def error(self, p):
        if self.lexer.text == '\n':
            return
        if not p:
            print("Syntax error at End of File!")
            return
        print("Syntax error at " + p.value)
