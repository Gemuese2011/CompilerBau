'''
Compiler Main
'''
from parserfile import MyParser
from lexerfile import MyLexer


def __init__(self):
    self.names = {}

if __name__ == '__main__':
    print("Initializing Bier Lexer")
    lexer = MyLexer()
    print("Initializing Bier Parser")
    parser = MyParser(lexer)
    print("Interpreting .bier File")
    print("========================Running Code========================")
    print()
    with open("main.bier", "r") as file:
        for text in file:
            if text:
                parser.parse(lexer.tokenize(text))

    lexer = MyLexer()
