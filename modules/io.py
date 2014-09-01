import re
import string
import sys

from parsetools import *

from modules.error import *

def out(source):
    i = 0

    i += len(out.__name__)
    i += eat_space(source[i:])

    output = ''

    # string to output
    if source[i] == '\'':
        i += 1

        while source[i] != '\'':
            output += source[i]
            i += 1

            # newline means unterminated string, fatal
            if source[i] == '\n':
                err_fatal('Unterminated string')

        # compensate for trailing single quote
        i += 1

    # non-string
    elif re.search(r"^[a-z]", source[i:]):
        variable_name = re.compile('^([a-z]+)').search(source[i:]).groups()[0]

        try:
            output = globals.symbol_table['variables'][variable_name]
            i += len(variable_name)
        except KeyError:
            err_fatal('Variable not found')

    output = string.replace(output, '\\n', '\n')

    sys.stdout.write(output)

    return i