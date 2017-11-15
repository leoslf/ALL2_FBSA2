import re
from .debug import *

def escapeSQLi(user_input: str) -> str:
    """
    escapeSQLi
    A very simple implementation of SQL injection prevention


    Parameters
    ----------------
    user_input : str
        Potentially unclean user input

    Returns
    ----------------
    str
        the string that has been tried to sanitize
    """
    debug("original: %r", user_input)
    ret = re.sub(r"('|\"|/\*|\*/|-- |;)", "", user_input)
    debug("sanitized: %r", ret)
    return ret
 


