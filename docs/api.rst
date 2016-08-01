Yassh API
============

The best place to start is the examples folder before diving into the API.

Reactor
-------------
.. autoclass:: yassh.Reactor
   :members:
   :inherited-members:
   :exclude-members: register_execution, unregister_execution

Local execution
---------------
.. autoclass:: yassh.LocalRun
   :members:
   :inherited-members:
   :exclude-members: fileno, process_output

.. autofunction:: yassh.local_run

Remote execution
----------------
.. autoclass:: yassh.RemoteRun
   :members:
   :inherited-members:
   :exclude-members: fileno, process_output

.. autofunction:: yassh.remote_run

Remote copy
-----------
.. autoclass:: yassh.RemoteCopy
   :members:
   :inherited-members:
   :exclude-members: fileno, process_output

.. autofunction:: yassh.remote_copy

Exceptions
----------
.. autoexception:: yassh.AlreadyStartedException
