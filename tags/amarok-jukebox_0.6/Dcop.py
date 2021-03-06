import os
import pcop
import pydcop

import Debug

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def call(call):
    Debug.log("DCOP call: " + call)
    f = os.popen("dcop amarok %s" % call)
    result = f.read()
    if f.close() is not None:
        raise Error
    result = result.strip()
    Debug.log("DCOP response: " + result)
    return result

def init():
    return pydcop.anyAppCalled("amarok")
