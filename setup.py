#!/usr/bin/env python

from setuptools import *

setup(
	name='dataflow',
	version='0.1.0',
	description='a dataflow library for python',
	author='Tim Cuthbertson',
	author_email='tim3d.junk+mocktest@gmail.com',
	url='http://github.com/gfxmonk/py-dataflow/tree',
	packages=find_packages(exclude=["test"]),
	
	long_description=open('readme.rst').read(),
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	keywords='dataflow concurrent concurrency',
	license='BSD',
	install_requires=[
		'setuptools',
	],
)
