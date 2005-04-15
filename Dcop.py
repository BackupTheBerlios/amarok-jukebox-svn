import os

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def call(call):
    command = "dcop amarok %s" % call
    #f = os.popen(command)
    #result = f.readline()
    #if f.close() is not None:
    #    raise Error
    #return result
    return os.popen(command)
