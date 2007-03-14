"""
utilities to deal with workingenvs:
http://svn.colorstudy.com/home/ianb/workingenv/workingenv.py
"""

import os
import subprocess

def activate(workingenv_location):
    """
    activate a workingenv
    """

    # update the python variables
    activate = os.path.join(workingenv_location, 'bin', 'activate')
    command = '. %s && env' % activate
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE, shell=True)
    env = process.communicate()[0]
    if process.returncode:
        raise OSError(
            "Command %r failed with error code %s"
            % (command, process.returncode))

    # update sys.path
    process = subprocess.Popen('. %s && python -c "import sys; print sys.path"' % activate, 
                               stdout=subprocess.PIPE, shell=True)
    pypath = process.communicate()[0]
    try:
        sys.path = eval(pypath)
    except Exception, e:
        raise e.__class__("Error %s while evaluating %r" % (e, pypath))

    
