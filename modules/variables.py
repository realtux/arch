import re
import pprint

import globals

def var(source):
    simple_assignment = re.compile('^var ([a-z0-9]+) \= \'(.+)\'\n').search(source)

    # simple assignment
    if simple_assignment:
        variable = simple_assignment.groups()[0]
        value = simple_assignment.groups()[1]

        globals.symbol_table['variables'][variable] = value

        i = 0
        while source[i] != '\n': i += 1

        return i