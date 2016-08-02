import logging

from .execution import Execution
from .reactor import Reactor

_logger = logging.getLogger(__name__)


class RemoteCopy(Execution):
    '''
    This class is used to copy a file from localhost
    to a remote host.
    '''

    def __init__(self, reactor, host, username,
                 local_path, remote_path,
                 logfile=None, remote_port=22):
        '''
        Create a new shell execution without starting it.

        :param Reactor reactor: The reactor used to execute monitors
        :param str host: The host used to run the shell execution
        :param str username: The username used to to run the shell execution
        :param str local_path: The file or directory local path
        :param str remote_path: The file or directory remote path
        :param file logfile: A file object used to log shell execution output
        :param int port: The ssh remote port number used
        '''
        super(RemoteCopy, self).__init__(reactor, logfile)

        self.__host = host
        self.__remote_port = remote_port
        self.__username = username
        self.__local_path = local_path.replace(u'"', u'\\"')
        self.__remote_path = remote_path.replace(u'"', u'\\"')

        _logger.debug('created copy "%s" -> "%s" on %s@%s:%d',
                      self.__local_path,
                      self.__remote_path,
                      self.__username,
                      self.__host,
                      self.__remote_port)

    def start(self):
        '''
        Start the execution.
        '''
        args = [u'-r',
                u'-P {0}'.format(self.__remote_port),
                u'-o BatchMode=yes',
                u'-o LogLevel=error',
                u'{0}'.format(self.__local_path),
                u'"{0}"@{1}:"{2}"'.format(self.__username,
                                          self.__host,
                                          self.__remote_path)]
        self._start(u'scp', args)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._terminate()


def remote_copy(host, username, local_path, remote_path,
                logfile=None,
                ms_timeout=-1,
                remote_port=22):
    '''
    Copy `local_path` to `remote_path` on `host` as `username`.

    Log execution output into `logfile` if not None.
    Wait `ms_timeout` for execution to complete.

    :param str host: The host used to run the shell execution
    :param str username: The username used to to run the shell execution
    :param str local_path: The file or directory local path
    :param str remote_path: The file or directory remote path
    :param file logfile: A file object used to log shell execution output
    :param int ms_timeout: Duration waited for an event to occur
    :param int remote_port: The ssh remote port number used
    :rtype: int
    :return: The execution result code
    '''
    r = Reactor()
    c = RemoteCopy(r, host, username, local_path, remote_path,
                   logfile=logfile,
                   remote_port=remote_port)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result
