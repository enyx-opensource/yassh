'''
The MIT License (MIT)

Copyright (c) 2016 EnyxSA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import logging
import uuid

from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class Copy(Execution):
    '''
    This class is used to copy a file from localhost
    to a remote host.

    Attributes
    ----------
    result : int
        The return code of the shell command.
    '''

    def __init__(self, name, reactor, host, username,
                 local_path, remote_path, logfile=None):
        '''
        Create a new shell command without starting it.

        Parameters
        ----------
        name : str
            The name of this command. Used by __repr__() method.
        reactor : ``Reactor``
            The reactor used to execute monitors.
        host : str
            The host used to run the shell command.
        username : str
            The username used to to run the shell command.
        local_path: str
            The file or directory local path.
        remote_path : str
            The file or directory remote path.
        logfile : stream
            A file object used to log shell command output.
        '''
        super(Copy, self).__init__(name, reactor, logfile)

        self.__host = host
        self.__username = username
        self.__local_path = local_path
        self.__remote_path = remote_path

        _logger.debug('created copy "%s" as "%s" -> "%s" on %s@%s',
                      name, local_path, remote_path, username, host)

    def start(self):
        '''
        Start the command.
        '''
        cmd = ('scp -r -o BatchMode=yes "{0}" '
               '"{1}"@{2}:"{3}"').format(self.__local_path,
                                         self.__username,
                                         self.__host,
                                         self.__remote_path)
        self._start(cmd)


def copy(host, username, local_path, remote_path, logfile=None, ms_timeout=-1):
    '''
    Copy ``local_path`` to ``remote_path`` on ``host`` as ``username``.

    Log command output into ``logfile`` if not None.
    Wait ``ms_timeout`` for command to complete.

    Returns:
    int
        The command result code.
    '''
    r = Reactor()
    c = Copy(uuid.uuid4(), r,
             host, username, local_path, remote_path, logfile)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
