from builtin import *

keywords = {
    'out': out
}

def eat_space(source):
    i = 0

    while source[i] == ' ': i += 1

    return i

def eat_comment(source):
    i = 0

    while source[i] != '-':
        i += 1

    return i

def is_keyword(source):
    for keyword in keywords:
        if source.startswith(keyword):
            return keyword

    return False

def handle_keyword(source):
    i = 0
    callable = ""

    for keyword in keywords:
        if source.startswith(keyword):
            callable = keyword
            break

    i += len(keyword)
    i += eat_space(source[i:])

    extracted_string = ""

    if source[i] == '\'':
        i += 1

        while source[i] != '\'':
            extracted_string += source[i]
            i += 1

    keywords[callable](extracted_string)
    return i