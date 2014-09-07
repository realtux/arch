from modules.io import *

def init():
    global line
    line = 1

    global symbol_table
    symbol_table = {
        'variables' : {}
    }

    global constructs
    constructs = {
        'out': out,
    }