from datetime import datetime
from .style import *


def info(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(f"{Style.BRIGHT}{date + ' ' if show else ''}[Info] {name}: {Style.NORMAL + message + Style.RESET}")


def warning(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(
        f"{Style.BRIGHT}{date + ' ' if show else ''}{Style.LIGHT_YELLOW}[Warning] {name}: {Style.NORMAL + message + Style.RESET}")


def error(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(
        f"{Style.BRIGHT}{date + ' ' if show else ''}{Style.LIGHT_RED}[Error] {name}: {Style.NORMAL + message + Style.RESET}")


def debug(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(
        f"{Style.BRIGHT}{date + ' ' if show else ''}{Style.LIGHT_BLUE}[Debug] {name}: {Style.NORMAL + message + Style.RESET}")
