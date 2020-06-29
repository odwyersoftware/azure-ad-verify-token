#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

LICENSE = (
    'Creative Commons Attribution-NonCommercial-NoDerivatives '
    '4.0 International License'
)

setup(
    name='azure-ad-verify-token',
    version='0.1.1',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    description='Verify JWT issued by Azure Active Directory B2C in Python.',
    author='O\'Dwyer Software',
    author_email='github@odwyer.software',
    url='https://github.com/odwyersoftware/azure-ad-verify-token',
    license=LICENSE,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
