import re
import string
import sys

from parsetools import *

from mod.error import *
from mod.lexer import *

def out(source):
    funcmeta = 0

    funcmeta += len(out.__name__)
    funcmeta += eat_space(source[funcmeta:])

    ccount, output = evaluate_expression(source[funcmeta:])

    # convert the text representations of the newline to a real newline
    output = string.replace(output, '\\n', '\n')

    sys.stdout.write(output)

    return funcmeta + ccount