import re

from parsetools import *

symbols = {}

axio_source = open('test.ax').read()
axio_lines = axio_source.split('\n')

i = 1

source = ''

for line in axio_lines:
    #print str(i) + ': ' + line
    i += 1

    source += str(line.strip()) + '-'

source = source[:-1]

i = 0

while i < len(source):
    if source[i] == ' ':
        i += eat_space(source[i:])
        continue

    elif source[i:].startswith('//'):
        i += eat_comment(source[i:])
        continue

    elif re.search(r"^[a-z]", source[i:]):
        if is_keyword(source[i:]):
            i += handle_keyword(source[i:])
            
    else:
        i += 1

# end execution
print ''