"""
functions having to do with python modules
"""

import os
import pkg_resources

def module_directory(module):
    """
    return the directory of a module
    """
    directory = pkg_resources.resource_filename(module, '')
    return directory.rstrip(os.sep)

def importable_name(name):
    try:
        components = name.split('.')
        start = components[0]
        g = globals()
        package = __import__(start, g, g)
        modulenames = [start]
        for component in components[1:]:
            modulenames.append(component)
            try:
                package = getattr(package, component)
            except AttributeError:
                n = '.'.join(modulenames)
                package = __import__(n, g, g, component)
        return package
    except ImportError:
        import traceback, cStringIO
        IO = cStringIO.StringIO()
        traceback.print_exc(file=IO)
        raise ValueError(
            'The object named by %r could not be imported\n%s' %  (
            name, IO.getvalue()))
