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

from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class RemoteCopy(Execution):
    '''
    This class is used to copy a file from localhost
    to a remote host.

    Attributes
    ----------
    result : int
        The return code of the shell execution.
    '''

    def __init__(self, reactor, host, username,
                 local_path, remote_path, logfile=None):
        '''
        Create a new shell execution without starting it.

        Parameters
        ----------
        reactor : ``Reactor``
            The reactor used to execute monitors.
        host : str
            The host used to run the shell execution.
        username : str
            The username used to to run the shell execution.
        local_path: str
            The file or directory local path.
        remote_path : str
            The file or directory remote path.
        logfile : stream
            A file object used to log shell execution output.
        '''
        super(RemoteCopy, self).__init__(reactor, logfile)

        self.__host = host
        self.__username = username
        self.__local_path = local_path.replace('"', r'\"')
        self.__remote_path = remote_path.replace('"', r'\"')

        _logger.debug(u'created copy "%s" -> "%s" on %s@%s',
                      local_path, remote_path, username, host)

    def start(self):
        '''
        Start the execution.
        '''
        cmd = ('scp -r -o BatchMode=yes "{0}" '
               '"{1}"@{2}:"{3}"').format(self.__local_path,
                                         self.__username,
                                         self.__host,
                                         self.__remote_path)
        self._start(cmd)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._terminate()


def remote_copy(host, username, local_path, remote_path,
                logfile=None, ms_timeout=-1):
    '''
    Copy ``local_path`` to ``remote_path`` on ``host`` as ``username``.

    Log execution output into ``logfile`` if not None.
    Wait ``ms_timeout`` for execution to complete.

    Returns:
    int
        The execution result code.
    '''
    r = Reactor()
    c = RemoteCopy(r, host, username, local_path, remote_path, logfile)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
