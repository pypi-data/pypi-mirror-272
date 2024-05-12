from .log import *
from .style import *
from .inputs import *
from time import sleep
from os import system

sleep = sleep
system = system


def print_line(char='-', width=54):
    try:
        char = str(char)
        width = int(width)
    except TypeError:
        raise TypeError("Char or Width must can convert to string or int")
    print(char * width)
