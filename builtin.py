import string
import sys

def out(output):
    output = string.replace(output, '\\n', '\n')

    sys.stdout.write(output)