import os
import re
from setuptools import setup

HERE = os.path.dirname(__file__)

def readme():
    return open(os.path.join(HERE, 'README.md')).read()

def version():
    with open(os.path.join(HERE, 'yassh', '__init__.py')) as f:
        return re.search(r"__version__ = '([^']+)'", f.read()).group(1)

setup(
    name = 'yassh',
    version = version(),
    install_requires = [
        "pexpect"
    ],
    author = 'David Keller',
    author_email = 'david.keller@enyx.com',
    description = 'A process remote launcher.',
    license = 'BSD',
    keywords = 'process launcher',
    url = 'http://packages.python.org/',
    packages=['yassh'],
    platforms='UNIX',
    long_description=readme()
)

