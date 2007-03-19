import os
import pkg_resources
def module_directory(module):
    """
    return the directory of a module
    """
    directory = pkg_resources.resource_filename(module, '')
    return directory.rstrip(os.sep)
