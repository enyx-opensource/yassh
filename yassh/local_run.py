import logging
from .execution import Execution
from .reactor import Reactor

LOGGER = logging.getLogger(__name__)


class LocalRun(Execution):
    '''
    This class is used to run locally a shell execution.
    '''

    def __init__(self, reactor, cmd, logfile=None):
        '''
        Create a new shell execution without starting it.

        :param Reactor reactor: The reactor used to execute monitors
        :param str cmd: A binary or bash-compatible expression
        :param file logfile: A file object used to log shell execution output
        '''
        super(LocalRun, self).__init__(reactor, logfile)

        self.__cmd = cmd.replace(u'"', u'\\"')

        LOGGER.debug('created local run "%s"', cmd)

    def start(self):
        '''
        Start the execution.
        '''
        args = ['-c', '({0})< <(cat; pkill -P $$)'.format(self.__cmd)]
        self._start(u'bash', args)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._terminate()


def local_run(cmd, logfile=None, ms_timeout=-1):
    '''
    Run `cmd`.

    Log execution output into `logfile` if not None.
    Wait `ms_timeout` for execution to complete.

    :param str cmd: str A binary or bash-compatible expression
    :param file logfile: A file object used to log shell execution output
    :param int ms_timeout: Duration waited for an event to occur
    :rtype: int
    :return: The execution result code
    '''
    reactor = Reactor()
    proc = LocalRun(reactor, cmd, logfile)

    with proc:
        while reactor.run(ms_timeout) > 0:
            pass

    return proc.result
