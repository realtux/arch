import re

import globals
import parsetools

import mod.error
import mod.constructs

# main lexer
def lexer(source):
    i = 0

    while i < len(source):
        # eat all space encountered that isn't part of a string
        if source[i] == ' ':
            i += parsetools.eat_space(source[i:])
            continue

        # end of line, push past and increment line
        elif source[i] == '\n':
            i += 1
            globals.line += 1
            continue

        # comment, eat text up to newline
        elif source[i:].startswith('//'):
            #print globals.line, source[i:3]
            i += parsetools.eat_comment(source[i:])
            continue

        # constructs (assignments)
        elif re.search(r"^var [a-zA-Z0-9_]+\s*=\s*.+\n", source[i:]):
            i += mod.constructs.handle_assignment(source[i:])

        # constructs (if)
        elif re.search(r"^if", source[i:]):
            i += 2
            i += mod.constructs.handle_if(source[i:])

        # constructs (out)
        elif re.search(r"^out", source[i:]):
            i += 3
            i += mod.constructs.handle_construct(source[i:], 'out')

        # function
        elif re.search(r"^[a-zA-Z_]\s*\(", source[i:]):
            pass

        # stop lexing at the end of whatever block it's in
        elif source[i] == '}':
            i += 1
            break

        else:
            mod.error.err_fatal('Unrecognized symbol "' + str(source[i]) + '"')

    return i

# expression evaluator
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

        # integer assignment
        elif re.search(r"^[0-9]+", expression[chars_eaten:]):
            integer = re.search(r"^([0-9]+)", expression[chars_eaten:]).groups()[0]

            expression_buffer = int(integer)

            chars_eaten += len(integer)

        # function
        elif re.search(r"^[a-zA-Z]+\(\s*(.+?)\s*\)", expression[chars_eaten:]):
            function_contents = re.search(r"^[a-zA-Z]+\(\s*(.+?)\s*\)", expression[chars_eaten:]).groups()[0]

        # variable
        elif re.search(r"^([a-zA-Z][a-zA-Z0-9_]+?)", expression[chars_eaten:]):
            variable_name = re.search(r"^([a-zA-Z0-9_]+)", expression[chars_eaten:]).groups()[0]

            try:
                result = globals.symbol_table['variables'][variable_name]

                if type(result) is int:
                    try:
                        expression_buffer = int(expression_buffer) + result
                    except ValueError:
                        expression_buffer = result

                else:
                    expression_buffer = expression_buffer + result
            except KeyError:
                mod.error.err_warning('Undefined variable')

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