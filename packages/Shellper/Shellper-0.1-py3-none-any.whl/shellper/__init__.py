from shellper import log
from shellper import inputs
from time import sleep


def print_line(char='-', width=54):
    try:
        char = str(char)
        width = int(width)
    except TypeError:
        raise TypeError("Char or Width must can convert to string or int")
    print(char * width)