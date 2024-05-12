from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)


def info(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise TypeError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(f"{Style.BRIGHT}{date+' ' if show else ''}[Info] {name}: {Style.NORMAL + message}")


def warning(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise TypeError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(f"{Style.BRIGHT}{date+' ' if show else ''}{Fore.YELLOW}[Warning] {name}: {Style.NORMAL + message}")


def error(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise TypeError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(f"{Style.BRIGHT}{date+' ' if show else ''}{Fore.RED}[Error] {name}: {Style.NORMAL + message}")


def debug(name, message, show: bool = True):
    try:
        name = str(name)
        message = str(message)
    except TypeError:
        raise TypeError("Name or message must can convert to string")
    date = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print(f"{Style.BRIGHT}{date+' ' if show else ''}{Fore.BLUE}[Debug] {name}: {Style.NORMAL + message}")
