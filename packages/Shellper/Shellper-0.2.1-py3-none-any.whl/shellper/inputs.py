from .log import *
from .style import *
from os import system


def inputs(word=Style.BRIGHT + ">>> " + Style.NORMAL, spilt_text=None, end_symbol: str = None, is_cmd: bool = False):
    try:
        word = str(word)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    text = input(word)
    if end_symbol is not None:
        if text[-1] == end_symbol:
            text = text[:-1]
        else:
            error("System", f"The last character of your command must be '{end_symbol}'.{Style.RESET}")
            return False
    if is_cmd:
        system(word)
    else:
        return text.split(spilt_text)
