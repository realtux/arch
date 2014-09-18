import sys
import re

import globals
import parsetools

import mod.error
import mod.lexer

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

# kick it off
mod.lexer.lexer(source)

# end execution
print ''