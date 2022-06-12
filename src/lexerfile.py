'''
Lex File
'''
from sly import Lexer


class MyLexer(Lexer):
    '''
    Lexer for Bier Compiler
    '''

    def __init__(self):
        pass

    tokens = {VARIABLE_NAME, VARIABLE_PREFIX, VAR_TYPE, STRING_VALUE, INTEGER_VALUE, FLOAT_VALUE, IS, PRINT, VARIABLES, NAMES, ASSIGN,
              LPAREN, RPAREN, COLON, CONSTANTS_PREFIX, COMMENT, CAST, TO, ARRAY, OF, R_SQUARE_BRACKETS, L_SQUARE_BRACKETS,
              COMMA, WITH, IF, THEN, ELSE, WHILE, EQ, NEQ, GT, LT, GE, LE, DO,}
    literals = {'=', '+', '-', '*', '/', '(', ')'}

    ignore = ' \t'

    # Tokens

    VARIABLE_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    R_SQUARE_BRACKETS = r'\]'
    L_SQUARE_BRACKETS = r'\['
    COLON = r':'
    COMMENT = r'\#.*'
    COMMA = r','
    STRING_VALUE = r'\".*\"'
    FLOAT_VALUE = r'[-+]?[0-9]*\.?[0-9]+'
    INTEGER_VALUE = r'[+-]?[0-9]+'


    # Special Names
    VARIABLE_NAME['var'] = VARIABLE_PREFIX
    VARIABLE_NAME['VAR'] = VARIABLE_PREFIX
    VARIABLE_NAME['const'] = CONSTANTS_PREFIX
    VARIABLE_NAME['CONST'] = CONSTANTS_PREFIX
    VARIABLE_NAME['IS'] = IS
    VARIABLE_NAME['is'] = IS
    VARIABLE_NAME['bool'] = VAR_TYPE
    VARIABLE_NAME['int'] = VAR_TYPE
    VARIABLE_NAME['String'] = VAR_TYPE
    VARIABLE_NAME['float'] = VAR_TYPE
    VARIABLE_NAME['char'] = VAR_TYPE
    VARIABLE_NAME['print'] = PRINT
    VARIABLE_NAME['all_vars'] = VARIABLES
    VARIABLE_NAME['all_names'] = NAMES

    VARIABLE_NAME['cast'] = CAST
    VARIABLE_NAME['CAST'] = CAST
    VARIABLE_NAME['TO'] = TO
    VARIABLE_NAME['to'] = TO
    VARIABLE_NAME['Array'] = ARRAY
    VARIABLE_NAME['array'] = ARRAY
    VARIABLE_NAME['OF'] = OF
    VARIABLE_NAME['of'] = OF
    VARIABLE_NAME['with'] = WITH
    VARIABLE_NAME['WITH'] = WITH

    VARIABLE_NAME['if'] = IF
    VARIABLE_NAME['then'] = THEN
    VARIABLE_NAME['else'] = ELSE
    VARIABLE_NAME['while'] = WHILE
    VARIABLE_NAME['equals'] = EQ
    VARIABLE_NAME['not_equal'] = NEQ
    VARIABLE_NAME['greater_than'] = GT
    VARIABLE_NAME['less_than'] = LT
    VARIABLE_NAME['greater_equal'] = GE
    VARIABLE_NAME['less_equal'] = LE
    VARIABLE_NAME['do'] = DO


    def error(self, t):
        '''
        Lexer Error Function
        :param t: readed Token
        '''
        print("Illegal character \"" + t.value[0] + "\" in line " + str(self.lineno))
        self.index += 1

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def get_line_no(self):
        '''
        Getter for line number
        :return: line_no
        '''
        return self.lineno


    #@_(r'\d+')
    #def NUMBER(self, t):
    #    t.value = int(t.value)
    #    return t


