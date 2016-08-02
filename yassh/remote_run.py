import logging

from .exceptions import AlreadyStartedException
from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class RemoteRun(Execution):
    '''
    This class is used to run a shell execution.
    '''

    def __init__(self, reactor, host, username, cmd,
                 logfile=None, remote_port=22):
        '''
        Create a new shell execution without starting it.

        :param Reactor reactor: The reactor used to execute monitors
        :param str host: The host used to run the shell execution
        :param str username: The username used to to run the shell execution
        :param str cmd: str A binary or bash-compatible expression
        :param file logfile: A file object used to log shell execution output
        :param int remote_port: The ssh remote port number used
        '''
        super(RemoteRun, self).__init__(reactor, logfile)

        self.__host = host
        self.__remote_port = remote_port
        self.__username = username
        self.__cmd = cmd.replace(u'"', u'\\"')

        _logger.debug('created remote run "%s" on %s@%s:%d',
                      self.__cmd,
                      self.__username,
                      self.__host,
                      self.__remote_port)

    def start(self):
        '''
        Start the execution.
        '''
        args = [u'-p {0}'.format(self.__remote_port),
                u'-o BatchMode=yes',
                u'-o LogLevel=error',
                u'{0}@{1}'.format(self.__username, self.__host),
                u'bash -c "({0})< <(cat; pkill -P $$)"'.format(self.__cmd)]
        self._start(u'ssh', args)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._send_eof()


def remote_run(host, username, cmd,
               logfile=None,
               ms_timeout=-1,
               remote_port=22):
    '''
    Run `cmd` on `host` as `username`.

    Log execution output into `logfile` if not None.
    Wait `ms_timeout` for execution to complete.

    :param str host: The host used to run the shell execution
    :param str username: The username used to to run the shell execution
    :param str cmd: str A binary or bash-compatible expression
    :param file logfile: A file object used to log shell execution output
    :param int ms_timeout: Duration waited for an event to occur
    :param int remote_port: The ssh remote port number used
    :rtype: int
    :return: The execution result code
    '''
    r = Reactor()
    c = RemoteRun(r, host, username, cmd,
                  logfile=logfile,
                  remote_port=remote_port)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
