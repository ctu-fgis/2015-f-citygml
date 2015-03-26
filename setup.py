#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from citygml2stl import __version__

setup(
    name='citygml2stl',
    version=__version__,
    description='CityGML to printable STL',
    long_description=''.join(open('README.rst').readlines()),
    keywords='3D printing, STL, mesh, CityGML',
    author='Miro Hrončok',
    author_email='miro@hroncok.cz',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
