#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, 'git_wipe', '__version__.py')) as f:
    exec(f.read(), about)

required = [
    'crayons',
    'click>=6.7',
    'blindspin>=2.0.1',
    'pygithub'
]

setup(
    name='git-wipe',
    version=about['__version__'],
    description='CLI tool for deleting Github branches',
    long_description=long_description,
    author='Povilas Susinskas',
    author_email='povilassusinskas@gmail.com',
    py_modules=['git_wipe'],
    packages=['git_wipe'],
    install_requires=required,
    entry_points={
        'console_scripts': ['git-wipe=git_wipe:cli'],
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
