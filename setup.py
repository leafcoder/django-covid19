#!/usr/bin/env python

import setuptools

with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f]

setuptools.setup(
    install_requires=install_requires
)
