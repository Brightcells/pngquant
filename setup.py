# -*- coding: utf-8 -*-

from __future__ import with_statement
from setuptools import setup


version = '1.0.4'


setup(
    name='pngquant',
    version=version,
    keywords='',
    description="A Python Wrapper of pngquant",
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/pngquant',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pngquant'],
    py_modules=[],
    install_requires=['Pillow', ],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
