import re

import globals

import mod.error
import mod.lexer

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

def handle_assignment(source):
    assignment = re.compile('^var ([a-zA-Z0-9_]+)\s*\=\s*(.+)\n').search(source)

    # assignment
    if assignment:
        variable = assignment.groups()[0]
        expression = assignment.groups()[1]

        ccount, result = mod.lexer.evaluate_expression(expression)

        globals.symbol_table['variables'][variable] = result

        i = 0
        while source[i] != '\n': i += 1

        return i

def handle_if(source):
    operators = [
        '==',
        '===',
        '!=',
        '<=',
        '>=',
    ]

    chars_eaten = 0;

    if_expression = re.compile(r"\((.+[^=!<>])([=!<>]+)(.+)\)").search(source);

    if if_expression:
        operator = if_expression.groups()[1]

        if not operator in operators:
            err_fatal('Invalid conditional operator')

        ccount, expression1 = mod.lexer.evaluate_expression(if_expression.groups()[0])
        chars_eaten += ccount
        ccount, expression2 = mod.lexer.evaluate_expression(if_expression.groups()[2])
        chars_eaten += ccount

    operation = False

    # resolve operator
    if operator == '==':
        if expression1 == expression2:
            chars_eaten += 2
            operation = True

    elif operator == '===':
        if expression1 is expression2:
            chars_eaten += 3
            operation = True

    elif operator == '!=':
        if expression1 != expression2:
            chars_eaten += 2
            operation = True

    # eat space up to opening {
    while (source[chars_eaten] != '{'):
        chars_eaten += 1

    chars_eaten += 1

    if operation == True:
        chars_eaten += mod.lexer.lexer(source[chars_eaten:])
    else:
        nested_ifs = 0

        while source[chars_eaten] != '}' or nested_ifs != 0:
            if source[chars_eaten] == '\n':
                chars_eaten += 1
                globals.line += 1

            elif source[chars_eaten] == '{':
                chars_eaten += 1
                nested_ifs += 1

            elif source[chars_eaten] == '}':
                chars_eaten += 1
                nested_ifs -= 1

            else:
                chars_eaten += 1

    return chars_eaten + 1