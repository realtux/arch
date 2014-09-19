import re
import string
import sys

import parsetools

import mod.error
import mod.lexer

def out(source):
    funcmeta = 0

    funcmeta += len(out.__name__)
    funcmeta += parsetools.eat_space(source[funcmeta:])

    ccount, output = mod.lexer.evaluate_expression(source[funcmeta:])

    # convert the text representations of the newline to a real newline
    output = string.replace(output, '\\n', '\n')

    sys.stdout.write(output)

    return funcmeta + ccount