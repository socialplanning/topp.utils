
import os
import subprocess

def abspath(path):
    return os.path.abspath(os.path.expanduser(path))

def makedir(dirname):
    """ 
    make directory if it does not already exist
    """

    if os.path.lexists(dirname):
        if os.path.isdir(dirname):
            return
        raise OSError('%s exists but is not a directory' % dirname)
    os.makedirs(dirname)

def get_args(command):
    """ return a list of args from a shell command using subprocess """

    arglist = subprocess.Popen('for i in %s; do echo $i; done' % command, 
                               shell=True,          
                               stdout=subprocess.PIPE).communicate()[0]
    arglist = [i for i in arglist.split('\n') if i]
    return arglist

def which(executable):
    """
    front-end to unix 'which'
    """

    process = subprocess.Popen(['which', executable], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    retval = process.communicate()[0]
    retval = retval.strip()

    if process.poll() or not retval:
        return None

    return retval
