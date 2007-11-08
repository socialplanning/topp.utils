from setuptools import Command
import pkg_resources
from pkg_resources import resource_filename, Requirement
import os
import shutil


class zinstall(Command):
    description = 'installs slugs for a particular zope instance'
    user_options = [('path', 'p', 'path to zope instance'),]
    command_consumes_arguments = True
    
    def initialize_options(self):
        self.args = None
        self.distname = self.distribution.get_name()

    def finalize_options(self):
        pass

    def _req_name(self):
        return str(self.distribution)
    
    def run(self):
        path = None
        if len(self.args)==1:
            path = self.args.pop()
        instance_path = get_path(path)
        req = Requirement.parse(self.distname)

        for filename in 'meta', 'overrides', 'configure',:
            fn = resource_filename(req, '%s-%s.zcml' %(self.distname, filename))
            if os.path.exists(fn):
                shutil.copy(fn, instance_path)


def get_path(start):
    end = 'etc/package-includes'
    if start:
        path = os.join(start, end)
        if os.path.exists(path):
            return path
        else:
            print "Path %s not found" %path

    for env in 'VIRTUAL_ENV', 'WORKING_ENV',:
        if os.environ.has_key(env):
            path = os.path.join(os.environ[env], 'zope', end)
            if os.path.exists(path):
                return path
    print "No path to zope found. Please enter a path to a zope instance"
