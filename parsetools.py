import re
import pprint

import globals

from modules.error import *

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
    assignment = re.compile('^var ([a-zA-Z0-9_]+)\s*\=\s*(.+)\n').search(source)

    # assignment
    if assignment:
        variable = assignment.groups()[0]
        expression = assignment.groups()[1]

        ccount, result = evaluate_expression(expression)

        globals.symbol_table['variables'][variable] = result

        i = 0
        while source[i] != '\n': i += 1

        return i

def evaluate_expression(expression):
    chars_eaten = 0
    expression_buffer = ''

    while True:
        # string assignment
        if re.search(r"^\'(.+)\'", expression[chars_eaten:]):
            string = re.search(r"^\'(.+?)\'", expression[chars_eaten:]).groups()[0]

            expression_buffer = expression_buffer + string

            # trim the buffer off the original expression
            chars_eaten += len(string) + 2

        # function
        elif re.search(r"^[a-zA-Z]+\(\s*(.+?)\s*\)", expression[chars_eaten:]):
            function_contents = re.search(r"^[a-zA-Z]+\(\s*(.+?)\s*\)", expression[chars_eaten:]).groups()[0]

        # variable
        elif re.search(r"^([a-zA-Z0-9_]+)", expression[chars_eaten:]):
            variable_name = re.search(r"^([a-zA-Z0-9_]+)", expression[chars_eaten:]).groups()[0]

            try:
                result = globals.symbol_table['variables'][variable_name]
            except KeyError:
                err_fatal('Undefined variable')

            expression_buffer = expression_buffer + result

            chars_eaten += len(variable_name)

        # concatenation
        elif re.search(r"^~", expression[chars_eaten:]):
            ccount, string = evaluate_expression(expression[chars_eaten + 1:])

            expression_buffer = expression_buffer + string
            chars_eaten += ccount + 1

        # eat space
        elif re.search(r"^ ", expression[chars_eaten:]):
            chars_eaten += 1

        # nothing left to evaluate
        else: return (chars_eaten, expression_buffer)

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