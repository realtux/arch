import globals

def err_fatal(message):
    print '\n','Arch Fatal:', message, 'at line', str(globals.line)
    quit()

def err_warning(message):
    print '\n','Arch Warning:', message, 'at line', str(globals.line)