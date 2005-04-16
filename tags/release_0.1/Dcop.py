import os

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def call(call):
    f = os.popen("dcop amarok %s" % call)
    result = f.readline()
    if f.close() is not None:
        raise Error
    return result.strip()
