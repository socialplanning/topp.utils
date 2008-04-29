from setuptools import setup, find_packages
import sys, os

version = '0.5'

f = open('README.txt')
readme = "".join(f.readlines())
f.close()

setup(name='topp.utils',
      version=version,
      description="utility library used for openplans.org",
      long_description=readme,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='topp openplans',
      author='The Open Planning Project',
      author_email='info@openplans.org',
      url='https://svn.openplans.org/svn/topp.utils',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['topp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "python-dateutil",
          "zope.dottedname"
          ],
      entry_points="""
      # -*- Entry points: -*-
      [distutils.commands]
      zinstall = topp.utils.setup_command:zinstall      
      [console_scripts]
      pytroff = topp.utils.modules:uninstall_package
      """,
      )
