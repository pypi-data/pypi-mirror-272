#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

try:
   import pypandoc
   README = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
   README = open('README.md').read()

setup(
    name='lo2',
    version='0.5.4',
    #url='none',
    author='DUHP BSP Team',
    author_email='zhangte01@baidu.com',
    description='lo2 - Log Oracle, an Oracle test language for log description and analysis',
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(),    
    install_requires=[
                        "Jinja2==3.1.2",
                        "ply>=3",
                        "chardet>=2.0",
                        "matplotlib>=3.5",
                    ],
)
