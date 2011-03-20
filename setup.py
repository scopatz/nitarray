#!/usr/bin/env python
 
from distutils.core import setup
from setuptools.command.develop import develop
#from distutils.extension import Extension

setup(name="nitarray",
	version='0.1',
	description="N-sized bit arrays",
	author='Anthony Scopatz',
	author_email='scopatz@gmail.com',
	url='http://www.scopatz.com/',
	packages=['nitarray'],
	package_dir={'nitarray': 'nitarray'}, 
	)

