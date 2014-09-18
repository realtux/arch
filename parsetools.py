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