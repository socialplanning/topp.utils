import subprocess

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
