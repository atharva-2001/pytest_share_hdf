#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-share_hdf',
    version='0.1.0',
    author='Atharva Arya',
    author_email='',
    maintainer='Atharva Arya',
    maintainer_email='',
    license='BSD-3',
    url='https://github.com/atharva-2001/pytest_share_hdf',
    description='Plugin to save test data in HDF files and retrieve them for comparison',
    long_description=read('README.md'),
    py_modules=['pytest_share_hdf.plugin'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0', 'numpy', 'pandas', 'tables'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'share_hdf = pytest_share_hdf.plugin',
        ],
    },
)
