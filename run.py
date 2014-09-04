import sys
import re

import globals

from parsetools import *
from modules.error import *

globals.init()

try:
    arch_source = open(sys.argv[1]).read()
except IOError:
    err_fatal('File could not be opened')
except IndexError:
    err_fatal('File could not be opened')

arch_lines = arch_source.split('\n')

i = 1

source = ''

# remove all whitespace and string commands end to end
for sourceline in arch_lines:
    #print str(i) + ': ' + sourceline
    i += 1

    source += str(sourceline.strip()) + '\n'

i = 0

# main lexer, parse every letter
while i < len(source):
    # eat all space encountered that isn't part of a string
    if source[i] == ' ':
        i += eat_space(source[i:])
        continue

    # end of command, push past
    elif source[i] == ';':
        i += 1
        continue

    # end of line, push past and increment line
    elif source[i] == '\n':
        i += 1
        globals.line += 1
        continue

    # comment, eat text up to newline
    elif source[i:].startswith('//'):
        print source[i:i+3]
        i += eat_comment(source[i:])
        continue

    # keywords, functions, variables
    elif re.search(r"^[a-z]", source[i:]):
        if is_keyword(source[i:]):
            i += handle_keyword(source[i:])
        else:
            err_fatal('Unrecognized symbol')

    else:
        err_fatal('Unrecognized symbol')

# end execution
print ''