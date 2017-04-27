#!/usr/bin/env python

import os
import re
from setuptools import setup

HERE = os.path.dirname(__file__)


def _readme():
    with open(os.path.join(HERE, 'README.rst')) as f:
        return f.read()


def _version():
    with open(os.path.join(HERE, 'yassh', '__init__.py')) as f:
        return re.search(r"__version__ = '([^']+)'", f.read()).group(1)

setup(
    name='yassh',

    version=_version(),

    description='A remote process launcher.',
    long_description=_readme(),

    url='https://github.com/enyx-opensource/yassh.git',

    author='David Keller',
    author_email='david.keller@enyx.com',

    license='BSD',

    keywords='process launcher',

    install_requires=[
        'pexpect',
    ],

    tests_require=[
        'sure', 'behave', 'coverage',
    ],

    packages=['yassh'],
    platforms='UNIX'
)
