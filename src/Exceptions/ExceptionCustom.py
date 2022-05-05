import os


class ExceptionCustom(Exception):
    def __init__(self, message):
        os.system('cls')
        super().__init__(message)