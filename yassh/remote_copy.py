import logging

from .execution import Execution
from .reactor import Reactor

LOGGER = logging.getLogger(__name__)


class RemoteCopy(Execution):
    '''
    This class is used to copy a file from localhost
    to a remote host.
    '''

    def __init__(self, reactor, remote,
                 local_path, remote_path,
                 logfile=None):
        '''
        Create a new shell execution without starting it.

        :param Reactor reactor: The reactor used to execute monitors
        :param RemoteConfiguration remote: The remote configuration
        :param str local_path: The file or directory local path
        :param str remote_path: The file or directory remote path
        :param file logfile: A file object used to log shell execution output
        '''
        super(RemoteCopy, self).__init__(reactor, logfile)

        self.__remote = remote
        self.__local_path = local_path.replace(u'"', u'\\"')
        self.__remote_path = remote_path.replace(u'"', u'\\"')

        LOGGER.debug('created copy "%s" -> "%s" on %s with options %s',
                     self.__local_path,
                     self.__remote_path,
                     self.__remote.host,
                     str(self.__remote))

    def start(self):
        '''
        Start the execution.
        '''
        self.__remote.set('BatchMode', 'yes')
        self.__remote.set('LogLevel', 'error')
        args = self.__remote.get_args()
        args += [u'-r',
                 u'{0}'.format(self.__local_path),
                 u'{0}:{1}'.format(self.__remote.host, self.__remote_path)]
        self._start(u'scp', args)

    def stop(self):
        '''
        Stop the execution.
        '''
        self._terminate()


def remote_copy(remote, local_path, remote_path,
                logfile=None,
                ms_timeout=-1):
    '''
    Copy `local_path` to `remote_path` on `remote.host`

    Log execution output into `logfile` if not None.
    Wait `ms_timeout` for execution to complete.

    :param remote a RemoteConfiguration object
    :param str local_path: The file or directory local path
    :param str remote_path: The file or directory remote path
    :param file logfile: A file object used to log shell execution output
    :param int ms_timeout: Duration waited for an event to occur
    :rtype: int
    :return: The execution result code
    '''
    reactor = Reactor()
    proc = RemoteCopy(reactor, remote, local_path, remote_path,
                      logfile=logfile)

    with proc:
        while reactor.run(ms_timeout) > 0:
            pass

    return proc.result
