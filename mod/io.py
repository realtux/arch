import re
import string
import sys

import parsetools

import mod.error
import mod.lexer

def out(source):
    i = 0

    i += parsetools.eat_space(source[i:])

    ccount, output = mod.lexer.evaluate_expression(source[i:])

    # convert the text representations of the newline to a real newline
    if type(output) is not int:
        output = string.replace(output, '\\n', '\n')

    sys.stdout.write(str(output))

    return i + ccount