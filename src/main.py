'''
Compiler Main
'''
from parserfile import MyParser
from lexerfile import MyLexer

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    with open("code.tinf", "r") as file:
        while True:
            try:
                text = file.readline()
            except EOFError:
                pass
            if text:
                parser.parse(lexer.tokenize(text))
