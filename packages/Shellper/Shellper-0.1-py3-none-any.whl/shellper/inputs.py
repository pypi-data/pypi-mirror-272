from colorama import Style, init
from shellper import log

init(autoreset=True)


def inputs(word=Style.BRIGHT + ">>> " + Style.NORMAL, spilt_text=None, end_symbol: str = None):
    try:
        word = str(word)
    except TypeError:
        raise TypeError("Name or message must can convert to string")
    text = input(word)
    if end_symbol is not None:
        if text[-1] == end_symbol:
            text = text[:-1]
        else:
            log.error("System", f"The last character of your command must be '{end_symbol}'.")
            return False
    return text.split(spilt_text)
