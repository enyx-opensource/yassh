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
import pexpect

from .exceptions import AlreadyStartedException

_logger = logging.getLogger(__name__)


class Execution(object):
    '''
    This class is used to run a shell command.

    Attributes
    ----------
    result : int
        The return code of the shell command.
    '''

    def __init__(self, name, reactor, logfile):
        '''
        Create a new shell command without starting it.

        Parameters
        ----------
        name : str
            The name of this command. Used by __repr__() method.
        reactor : ``Reactor``
            The reactor used to execute monitors.
        cmd : str
            A binary or bash-compatible expression. (e.g. 'echo ok && sleep 1')
        logfile : stream
            A file object used to log shell command output.
        '''
        self.__name = name
        self.__reactor = reactor
        self.__exec = None

        self.__logfile = logfile

        self.__monitors = {}

        self.result = -1

        def on_exit(): self.__finalize()
        self.register_exit_monitor(on_exit)

        _logger.debug('created execution "%s"', name)

    def __del__(self):
        '''
        Stop the command uppon destruction.
        '''
        self.__finalize()

    def __enter__(self):
        '''
        Start the command uppon context enter.
        '''
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        Stop the command uppon context exit.
        '''
        self.__finalize()
        return False

    def __finalize(self):
        if not self.started():
            return

        self.__reactor.unregister_command(self)
        self.__exec.close()

        if self.__exec.exitstatus is not None:
            self.result = self.__exec.exitstatus

        self.__exec = None

        _logger.info('finalized %s (%d)', self, self.result)

    def _start(self, cmd):
        '''
        Start the command.
        '''
        if self.started():
            raise AlreadyStartedException()

        self.__exec = pexpect.spawnu(cmd)

        self.__reactor.register_command(self)

        _logger.info('started %s', self)

    def stop(self):
        '''
        The command is killed but any pending monitor(s)
        can still be called (e.g. on_exit)
        '''
        if not self.started():
            return

        self.__exec.terminate()

        _logger.info('terminated %s', self)

    def started(self):
        '''
        Check if the command is started.

        Returns
        -------
        bool
            True if started, False otherwise.
        '''
        return self.__exec is not None

    def fileno(self):
        '''
        Return the command output pipe fileno.

        Note
        ----
        This is used by the reactor.

        Returns
        -------
        int
            The pipe fileno.
        '''
        return self.__exec.fileno()

    def register_monitor(self, pattern, callback):
        '''
        Register a ``callback`` to be executed once the ``pattern`` has matched
        command output.

        Parameters
        ----------
        pattern : str
            A pattern to match.
        callback : function
            A callback to invoke.
        '''
        self.__monitors.setdefault(pattern, []).append(callback)

        _logger.debug('registered monitor "%s" on %s', pattern, self)

    def register_exit_monitor(self, callback):
        '''
        Register ``callback`` to be executed once the command has terminated.

        Parameters
        ----------
        callback : function
            A callback to invoke.
        '''
        self.register_monitor(pexpect.EOF, callback)

    def process_output(self):
        '''
        Try to match command output against registered monitor(s).
        '''
        patterns = [pexpect.TIMEOUT] + list(self.__monitors.keys())
        index = self.__exec.expect(patterns, timeout=0)

        if index:
            # ssh.before seems only valid when something
            # other that timeout matched.
            if self.__logfile:
                self.__logfile.write(self.__exec.before)

            self.__invoke_callbacks(patterns[index])

    def __repr__(self):
        '''
        Return the string represensation of the command.

        Returns:
            str: A string represensation of the command.
        '''
        return 'command "{0}"'.format(self.__name)

    def __invoke_callbacks(self, matched_pattern):
        _logger.debug('matched monitor "%s" on %s',
                      matched_pattern, self)

        for callback in self.__monitors[matched_pattern]:
            callback()
