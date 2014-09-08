import re

import globals

# chew up the space until the next character that isn't a space
# returns: number of spaces until the next character is hit
def eat_space(source):
    i = 0

    while source[i] == ' ': i += 1

    return i

def eat_comment(source):
    i = 0

    while source[i] != '\n':
        i += 1

    # return number of characters and push past the newline
    return i

def handle_assignment(source):
    assignment = re.compile('^var ([a-z0-9]+)\s*\=\s*(.+)\n').search(source)

    # assignment
    if assignment:
        variable = assignment.groups()[0]
        expression = assignment.groups()[1]

        evaluated_expression = evaluate_expression(expression)

        globals.symbol_table['variables'][variable] = evaluated_expression

        i = 0
        while source[i] != '\n': i += 1

        return i

def evaluate_expression(expression):
    # string assignment
    if re.search(r"^\'(.+)\'", expression):
        string = re.search(r"^\'(.+)\'", expression)

        return string.groups()[0]

def is_construct(source):
    for construct in globals.constructs:
        if source.startswith(construct):
            return construct

    return False

def handle_construct(source):
    for construct in globals.constructs:
        if source.startswith(construct):
            callable = construct
            break

    return globals.constructs[callable](source)