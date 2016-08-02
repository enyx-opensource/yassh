import logging
import errno
import select

_logger = logging.getLogger(__name__)


class Reactor(object):
    '''
    This class is used to execute execution(s) monitor(s).
    '''

    def __init__(self):
        '''
        Create a new reactor.
        '''
        self.poller = select.poll()
        self.fd_to_cmd = {}

    def register_execution(self, cmd):
        '''
        Register a new `cmd` on the reactor.

        This will allow reactor to monitor `cmd` output
        and execute `cmd` monitor accordingly.

        :param Execution cmd: The cmd to register
        '''
        self.poller.register(cmd.fileno(), select.POLLIN | select.POLLPRI)
        self.fd_to_cmd[cmd.fileno()] = cmd

        _logger.debug('registered %s', cmd)

    def unregister_execution(self, cmd):
        '''
        Unregister a `cmd`.

        :param Execution cmd: The cmd to unregister
        '''
        del self.fd_to_cmd[cmd.fileno()]
        self.poller.unregister(cmd)

        _logger.debug('unregistered %s', cmd)

    def _run(self, ms_timeout):
        if not len(self.fd_to_cmd):
            return 0

        count = self.poller.poll(ms_timeout)
        for fd, __ in count:
            cmd = self.fd_to_cmd.get(fd, None)

            _logger.debug('%s has new output', cmd)
            if cmd:
                cmd.process_output()

        return len(count)

    def run(self, ms_timeout):
        '''
        Wait `ms_timeout` for some registered execution(s) to generate
        output and execute associated monitor(s).

        :param int ms_timeout: Duration waited for an event to occur
        :rtype: int
        :return: The event(s) count
        '''
        try:
            return self._run(ms_timeout)
        except select.error as err:
            if err[0] == errno.EINTR:
                return 0
            raise
