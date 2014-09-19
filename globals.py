import mod.io

def init():
    global line
    line = 1

    global symbol_table
    symbol_table = {
        'variables' : {}
    }

    global constructs
    constructs = {
        'out': mod.io.out,
    }