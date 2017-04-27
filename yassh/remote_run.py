import logging

from .execution import Execution
from .reactor import Reactor

LOGGER = logging.getLogger(__name__)


class RemoteRun(Execution):
    '''
    This class is used to run a shell execution.
    '''

    def __init__(self, reactor, remote, cmd,
                 logfile=None):
        '''
        Create a new shell execution without starting it.

        :param Reactor reactor: The reactor used to execute monitors
        :param RemoteConfiguration remote: The remote configuration
        :param str cmd: str A binary or bash-compatible expression
        :param file logfile: A file object used to log shell execution output
        :param int remote_port: The ssh remote port number used
        '''
        super(RemoteRun, self).__init__(reactor, logfile)

        self.__remote = remote
        self.__cmd = cmd.replace(u'"', u'\\"')

        LOGGER.debug('created remote run "%s" with args "%s"',
                     self.__cmd,
                     remote)

    def start(self):
        '''
        Start the execution.
        '''
        self.__remote.set('BatchMode', 'yes')
        self.__remote.set('LogLevel', 'error')
        args = self.__remote.get_args()
        args.append(u'{host}'.format(host=self.__remote.host))
        args.append(u'bash -c "({0})< <(cat; pkill -P $$)"'.format(self.__cmd))
        self._start(u'ssh', args)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._send_eof()


def remote_run(remote, cmd,
               logfile=None,
               ms_timeout=-1):
    '''
    Run `cmd` on remote.host as remote.username

    Log execution output into `logfile` if not None.
    Wait `ms_timeout` for execution to complete.

    :param RemoteConfiguration remote: The connection parameters
    :param str cmd: str A binary or bash-compatible expression
    :param file logfile: A file object used to log shell execution output
    :param int ms_timeout: Duration waited for an event to occur
    :rtype: int
    :return: The execution result code
    '''
    reactor = Reactor()
    proc = RemoteRun(reactor=reactor, remote=remote, cmd=cmd, logfile=logfile)

    with proc:
        while reactor.run(ms_timeout) > 0:
            pass

    return proc.result
