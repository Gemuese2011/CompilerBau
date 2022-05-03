from sly import Lexer

class MyLexer(Lexer):

    def __init__(self):
        self.lineno = 0

    tokens = {VARIABLE_NAME, VARIABLE_PREFIX, VAR_TYPE, VARIABLE_VALUE, IS, PRINT, VARIABLES, NAMES, ASSIGN, LPAREN,
              RPAREN, COLON, CONSTANTS_PREFIX}
    ignore = ' \t'

    # Tokens
    VARIABLE_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    VARIABLE_VALUE = r'(\".*\"|[0-9]+)'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    COLON = r':'

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

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comment = '\# .*'

    def error(self, t):
        print("Illegal character '%s'" + t.value[0] + "in line " + self.lineno)
        self.index += 1

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
