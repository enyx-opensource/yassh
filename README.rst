.. image:: https://travis-ci.org/enyx-opensource/yassh.svg?branch=master
   :target: https://travis-ci.org/enyx-opensource/yassh
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/enyx-opensource/yassh/badge.svg?branch=master
   :target: https://coveralls.io/github/enyx-opensource/yassh?branch=master
   :alt: Coverage Status

.. image:: https://codeclimate.com/github/enyx-opensource/yassh/badges/gpa.svg
   :target: https://codeclimate.com/github/enyx-opensource/yassh
   :alt: Code Climate

.. image:: https://codeclimate.com/github/enyx-opensource/yassh/badges/issue_count.svg
   :target: https://codeclimate.com/github/enyx-opensource/yassh
   :alt: Issue Count

.. image:: https://readthedocs.org/projects/yassh/badge/?version=latest
   :target: http://yassh.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

yassh
=====

Yassh is a python library used to run
asynchronous, dependent remote and local tasks.

Usage
-----

.. code-block:: python

    import logging
    from yassh import Reactor, RemoteRun, LocalRun

    logging.basicConfig(level=logging.DEBUG)

    r = Reactor()
    c1 = RemoteRun(r, 'localhost', 'user', 'sleep 5')
    c2 = LocalRun(r, 'echo ok')
    c3 = RemoteRun(r, 'localhost', 'user', 'echo "finished" && sleep 1')

    # Start cmd2 when cmd1 complete
    def start_c2():
        c2.start()
    c1.register_exit_monitor(start_c2)

    # Start cmd3 when cmd2 complete
    def start_c3():
        c3.start()
    c2.register_monitor(u'ok', start_c3)

     # Print dummy message when c3 is near terminaison
    def on_c3_finished():
        print('c3 almost finished')
    c3.register_monitor(u'finished', on_c3_finished)

    # Start first task
    c1.start()

    timeout = -1 # Infinite
    while r.run(timeout) > 0:
            pass

Installation
------------

To install latest release::

    pip install yassh

To install latest code::

    pip install git+https://github.com/enyx-opensource/yassh.git

Testing
-------

Run from project root::

    behave

License
-------
MIT License (see LICENSE)

