from modules.io import *
from modules.variables import *

def init():
    global line
    line = 1

    global symbol_table
    symbol_table = {
        'variables' : {}
    }

    global keywords
    keywords = {
        'out': out,
        'var': var
    }