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

from .exceptions import AlreadyStartedException
from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class Command(Execution):
    '''
    This class is used to run a shell command.

    Attributes
    ----------
    result : int
        The return code of the shell command.
    '''

    def __init__(self, name, reactor, host, username, cmd, logfile=None):
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
        cmd : str
            A binary or bash-compatible expression. (e.g. 'echo ok && sleep 1')
        logfile : stream
            A file object used to log shell command output.
        '''
        super(Command, self).__init__(name, reactor, logfile)

        self.__host = host
        self.__username = username
        self.__cmd = cmd

        _logger.debug('created command "%s" as "%s" on %s@%s',
                      name, cmd, username, host)

    def start(self):
        '''
        Start the command.
        '''
        cmd = ('ssh -o BatchMode=yes "{0}"@{1} '
               '"({2})< <(cat; kill 0)"').format(self.__username,
                                                 self.__host,
                                                 self.__cmd)
        self._start(cmd)


def run(host, username, cmd, logfile=None, ms_timeout=-1):
    '''
    Run ``cmd`` on ``host`` as ``username``.

    Log command output into ``logfile`` if not None.
    Wait ``ms_timeout`` for command to complete.

    Returns:
    int
        The command result code.
    '''
    r = Reactor()
    c = Command(uuid.uuid4(), r,
                host, username, cmd, logfile)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
