"""
functions having to do with python modules
"""

import os
import pkg_resources
import shutil
import subprocess
import sys

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

def uninstall_package(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        package_name = argv[1]
    except IndexError:
        print "Usage: pytroff [PACKAGE]"
        return 1

    try:
        package = pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        print "Package %s doesn't seem to be installed." % package_name
        return 1

    location = package.location
    if location.endswith('.egg'):
        shutil.rmtree(location)
    else:
        # assume it's a development package
        current = os.getcwd()
        os.chdir(location)
        subprocess.Popen(['python', 'setup.py', 'develop', '--uninstall']).wait()
        os.chdir(current)
    
    print "Uninstalled package %s" % package_name
