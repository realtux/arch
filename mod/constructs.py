import re

import globals

import parsetools

import mod.error
import mod.lexer

def is_construct(source):
    for construct in globals.constructs:
        if source.startswith(construct):
            return construct

    return False

def handle_construct(source, construct):
    if construct in globals.constructs:
        callable = construct

    return globals.constructs[callable](source)

def handle_assignment(source):
    assignment = re.compile('^var ([a-zA-Z][a-zA-Z0-9_]+?)\s*\=\s*(.+)\n').search(source)

    # assignment
    if assignment:
        variable = assignment.groups()[0]
        expression = assignment.groups()[1]

        ccount, result = mod.lexer.evaluate_expression(expression)

        if type(result) is int:
            actual_result = int(result)
        else:
            actual_result = str(result)

        globals.symbol_table['variables'][variable] = actual_result

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

    chars_eaten += parsetools.eat_space(source)

    if_expression = re.compile(r"\((.+[^=!<>])([=!<>]+)(.+)\)").search(source);

    if if_expression:
        operator = if_expression.groups()[1]

        if not operator in operators:
            err_fatal('Invalid conditional operator')

        ccount, expression1 = mod.lexer.evaluate_expression(if_expression.groups()[0])
        ccount, expression2 = mod.lexer.evaluate_expression(if_expression.groups()[2])

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

    chars_eaten += parsetools.eat_parens_block(source[chars_eaten:])

    chars_eaten += parsetools.eat_space(source[chars_eaten:])

    # if statement must contain at least 1 block either way
    if source[chars_eaten] != '{':
        mod.error.err_parse('{ Expected')

    # process a true condition
    if operation == True:
        chars_eaten += 1
        chars_eaten += mod.lexer.lexer(source[chars_eaten:])

        # eat the remaining else block if present
        while True and chars_eaten < len(source):
            chars_eaten += parsetools.eat_space(source[chars_eaten:])

            if source[chars_eaten] == '\n':
                chars_eaten += 1
                globals.line += 1

            elif source[chars_eaten:].startswith('else'):
                chars_eaten += 4
                chars_eaten += parsetools.eat_space(source[chars_eaten:])

                if source[chars_eaten] == '{':
                    chars_eaten += parsetools.eat_braced_block(source[chars_eaten:])
                else:
                    mod.error.err_parse('{ Expected')

            else:
                break

    else:
        chars_eaten += parsetools.eat_braced_block(source[chars_eaten:])

        chars_eaten += parsetools.eat_space(source[chars_eaten:])

        if source[chars_eaten:].startswith("else"):
            chars_eaten += 4
            chars_eaten += parsetools.eat_space(source[chars_eaten:])

            if source[chars_eaten] == '{':
                chars_eaten += 1
                chars_eaten += mod.lexer.lexer(source[chars_eaten:])
            else:
                mod.error.err_parse('{ Expected')

    return chars_eaten