from setuptools import setup, find_packages
import sys, os

version = '0.2.7'

setup(name='topp.utils',
      version=version,
      description="",
      long_description="""\
""",
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
      install_requires=["python-dateutil"],
      entry_points="""
      # -*- Entry points: -*-
      
      """,
      )
