'''
Used for various common tasks.
'''
from dataclasses import dataclass

@dataclass
class Colours:
    '''Holds colours for the terminal.'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def empty(a: int|list|str) -> bool:
    '''
    Returns True if a is empty ("", [], "-", etc.).'''
    if isinstance(a, list):
        if len(a) == 0:
            return True
        for i in a:
            if not empty(i):
                return False
        return True
    if isinstance(a, str):
        return len(a) == 0 or a in ["-", " ", "."]
    if isinstance(a, int):
        return a == 0
    return False

def latinise(word: str):
    '''
    Converts a string to latin characters.
    '''
    # āçēīłṉōṟşūƶĀÇĒĪŁṈŌṞŞŪƵ
    word = word.replace("ā", "a" )
    word = word.replace("ç", "ch")
    word = word.replace("ē", "e" )
    word = word.replace("ī", "i" )
    word = word.replace("ł", "w" )
    word = word.replace("ṉ", "ny")
    word = word.replace("ō", "o" )
    word = word.replace("ṟ", "rw")
    word = word.replace("ş", "sh")
    word = word.replace("ū", "u" )
    word = word.replace("ƶ", "zh")
    word = word.replace("Ā", "A" )
    word = word.replace("Ç", "Ch")
    word = word.replace("Ē", "E" )
    word = word.replace("Ī", "I" )
    word = word.replace("Ł", "W" )
    word = word.replace("Ṉ", "Ny")
    word = word.replace("Ō", "O" )
    word = word.replace("Ṟ", "Rw")
    word = word.replace("Ş", "Sh")
    word = word.replace("Ū", "U" )
    word = word.replace("Ƶ", "Zh")
    return word
