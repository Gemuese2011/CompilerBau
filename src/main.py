'''
Compiler Main
'''
import pathlib
from os import listdir
from os.path import isfile, join

from parserfile import MyParser
from lexerfile import MyLexer

path = "./TestProgramme"


def get_programms():
    return [f for f in listdir(path) if (isfile(join(path, f)) and pathlib.Path(f).suffix == ".bier")]


def __init__(self):
    self.names = {}


if __name__ == '__main__':

    print("Choose Programm:")
    programms = get_programms()
    i = 0
    for file in programms:
        print(str(i) + ": " + file)
        i += 1

    number = int(input("Enter Filenumber: "))


    print("Initializing Bier Lexer")
    lexer = MyLexer()
    print("Initializing Bier Parser")
    parser = MyParser(lexer)
    print("Interpreting .bier File")
    print("========================Running Code========================")
    print()
    with open(path + "/" + programms[number], "r") as file:
        for text in file:
            if text:
                parser.parse(lexer.tokenize(text))

    lexer = MyLexer()
