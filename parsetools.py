import globals

import mod.error

def eat_space(source):
    i = 0
    try:
        while source[i] == ' ': i += 1
    except IndexError:
        return 0

    return i

def eat_comment(source):
    i = 0

    while source[i] != '\n':
        i += 1

    # return number of characters and push past the newline
    return i

def eat_braced_block(source):
    i = 1

    nested_braces = 0

    try:
        while source[i] != '}' or nested_braces != 0:
            if source[i] == '\n':
                i += 1
                globals.line += 1

            elif source[i] == '{':
                i += 1
                nested_braces += 1

            elif source[i] == '}':
                i += 1
                nested_braces -= 1

            else:
                i += 1
    except IndexError:
        mod.error.err_parse('} Expected')

    return i + 1

def eat_parens_block(source):
    i = 1

    nested_parens = 0

    try:
        while source[i] != ')' or nested_parens != 0:
            if source[i] == '(':
                i += 1
                nested_parens += 1

            elif source[i] == ')':
                i += 1
                nested_parens -= 1

            else:
                i += 1
    except IndexError:
        mod.error.err_parse(') Expected')

    return i + 1