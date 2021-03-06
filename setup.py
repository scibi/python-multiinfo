#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='python-multiinfo',
    version='0.1.0',
    description=('Python library for sending and receiving SMS messages with '
                 'MultiInfo service provided by Polkomtel'),
    long_description=readme + '\n\n' + history,
    author='Patryk Ściborek',
    author_email='patryk@sciborek.com',
    url='https://github.com/scibi/multiinfo',
    packages=[
        'multiinfo',
    ],
    package_dir={'multiinfo': 'multiinfo'},
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='multiinfo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
