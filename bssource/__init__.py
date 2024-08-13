import sys
import os
import inspect

# This is complicated due to the fact that __file__ is not always defined.

def GetScriptDirectory():
    
    if hasattr(GetScriptDirectory, "dir"):
        return GetScriptDirectory.dir
    module_path = ""
    try:

        # The easy way. Just use __file__.
        # Unfortunately, __file__ is not available when cx_freeze is used or in IDLE.
        if python2:
            module_path = str(os.path.abspath(inspect.getfile(GetScriptDirectory))) 
        else:
            module_path = __file__
    except NameError:
        if len(sys.argv) > 0 and len(sys.argv[0]) > 0 and os.path.isabs(sys.argv[0]):
            module_path = sys.argv[0]
        else:
            module_path = os.path.abspath(inspect.getfile(GetScriptDirectory))
            if not os.path.exists(module_path):
                # If cx_freeze is used the value of the module_path variable at this point is in the following format.
                # {PathToExeFile}\{NameOfPythonSourceFile}. This makes it necessary to strip off the file name to get the correct
                # path.
                module_path = os.path.dirname(module_path)
    GetScriptDirectory.dir = os.path.dirname(module_path)
    return GetScriptDirectory.dir

#dirname = os.path.dirname(__file__)
dirname = GetScriptDirectory()


# Make a backup of sys.path
old_sys_path = sys.path[:]


sys.path.insert(0, dirname)

from .calc import calc
from .bssource import *
