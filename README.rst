.. image:: https://travis-ci.org/Enyx-SA/yassh.svg?branch=master
   :target: https://travis-ci.org/Enyx-SA/yassh
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/Enyx-SA/yassh/badge.svg?branch=master
   :target: https://coveralls.io/github/Enyx-SA/yassh?branch=master
   :alt: Coverage Status

.. image:: https://codeclimate.com/github/Enyx-SA/yassh/badges/gpa.svg
   :target: https://codeclimate.com/github/Enyx-SA/yassh
   :alt: Code Climate

.. image:: https://codeclimate.com/github/Enyx-SA/yassh/badges/issue_count.svg
   :target: https://codeclimate.com/github/Enyx-SA/yassh
   :alt: Issue Count

yassh
=====

This project contains a python library used
to run asynchronous and dependent ssh tasks.

Usage
-----

.. code:: python

    import logging
    from yassh import *

    logging.basicConfig(level=logging.DEBUG)

    r = Reactor()
    c1 = Command('cmd1', r, 'localhost', 'user', 'sleep 5')
    c2 = Command('cmd2', r, 'localhost', 'user', 'echo ok')
    c3 = Command('cmd3', r, 'localhost', 'user', 'echo "finished" && sleep 1')

    # Start cmd2 when cmd1 complete
    def start_c2(): c2.start()
    c1.register_exit_monitor(start_c2)

    # Start cmd3 when cmd2 complete
    def start_c3(): c3.start()
    c2.register_monitor(u'ok', start_c3)

     # Print dummy message when c3 is near terminaison
    def on_c3_finished(): print 'c3 almost finished'
    c3.register_monitor(u'finished', on_c3_finished)

    # Start first task
    c1.start()

    timeout = -1
    while r.run(timeout) > 0:
            pass

Installation
------------

To install latest release::

    pip install yassh

To install latest code::

    pip install git+https://github.com/Enyx-SA/yassh.git

Testing
-------

Run from project root::

    behave

License
-------
MIT License (see LICENSE)

