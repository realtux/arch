import globals

def err_fatal(message):
    print '\n','Arch Fatal:', message, 'at line', str(globals.line)
    quit()