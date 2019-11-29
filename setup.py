from __future__ import print_function
from setuptools import setup, find_packages
# import subprocess
# import sys

from distutils.command.build_py import build_py
from distutils.command.build_scripts import build_scripts

import os
import sys
mydir = os.path.dirname(__file__)

with open('README.md') as f:
    long_description = f.read()

setup(
    name="pyftd2xx",
    version=0.91,
    packages=find_packages(),
    # metadata for upload to PyPI
    author="Julian Sp",
    description="Python interface to FTDI official driver d2xx",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="GNU GPLv3",
    keywords="ftd2xx pyftd2xx d2xx pyd2xx ftdi pyftdi wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/JulianS-Uni/pyftd2xx',  # project home page, if any
    install_requires=([])
)
