import os
from setuptools import setup

def readme():
    return open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(
    name = 'yassh',
    version = '0.1.0',
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
