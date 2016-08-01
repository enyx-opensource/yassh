Tutorial
========

Concurrent run
--------------
* Run 3 concurrent local processes.
* Register an exit monitor to ensure they succeed

.. literalinclude:: ../examples/concurrent.py

Dependant run
--------------
* Start both local and remote processes.
* Uppon first process exit, start second process and so one with third process.


.. literalinclude:: ../examples/dependent.py

