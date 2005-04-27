import os
import Debug

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def call(call):
    call = call.encode('utf-8')
    Debug.log("DCOP call: " + call)
    f = os.popen("dcop amarok %s" % call)
    result = f.readline()
    if f.close() is not None:
        raise Error
    result = result.strip()
    Debug.log("DCOP response: " + result)
    return result
