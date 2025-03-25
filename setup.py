# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.9'


setup(
    name='pngquant',
    version=version,
    keywords='',
    description='A Python Wrapper of pngquant',
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/pngquant',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pngquant'],
    py_modules=[],
    install_requires=['Pillow', 'puremagic', ],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
