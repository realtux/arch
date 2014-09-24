import globals

def err_fatal(message):
    print '\n','Arch Fatal:', message, 'at line', str(globals.line)
    quit()

def err_warning(message):
    print '\n','Arch Warning:', message, 'at line', str(globals.line)

def err_parse(message):
    print '\n','Arch Parse Error:', message, 'at line', str(globals.line)
    quit()