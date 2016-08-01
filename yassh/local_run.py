import logging
from locale import getpreferredencoding

from .exceptions import AlreadyStartedException
from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class LocalRun(Execution):
    '''
    This class is used to run locally a shell execution.

    Attributes
    ----------
    result : int
        The return code of the shell execution.
    '''

    def __init__(self, reactor, cmd, logfile=None):
        '''
        Create a new shell execution without starting it.

        Parameters
        ----------
        reactor : ``Reactor``
            The reactor used to execute monitors.
        cmd : str
            A binary or bash-compatible expression. (e.g. 'echo ok && sleep 1')
        logfile : stream
            A file object used to log shell execution output.
        '''
        super(LocalRun, self).__init__(reactor, logfile)

        self.__cmd = cmd.replace(u'"', u'\\"')

        _logger.debug('created local run "%s"', cmd)

    def start(self):
        '''
        Start the execution.
        '''
        self._start(self.__cmd)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._terminate()


def local_run(cmd, logfile=None, ms_timeout=-1):
    '''
    Run ``cmd``.

    Log execution output into ``logfile`` if not None.
    Wait ``ms_timeout`` for execution to complete.

    Returns:
    int
        The execution result code.
    '''
    r = Reactor()
    c = LocalRun(r, cmd, logfile)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
