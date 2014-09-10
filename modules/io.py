import re
import string
import sys

from parsetools import *

from modules.error import *

def out(source):
    funcmeta = 0

    funcmeta += len(out.__name__)
    funcmeta += eat_space(source[i:])

    ccount, output = evaluate_expression(source[i:])

    # convert the text representations of the newline to a real newline
    output = string.replace(output, '\\n', '\n')

    sys.stdout.write(output)

    return funcmeta + ccount