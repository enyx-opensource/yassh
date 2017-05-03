import logging
import errno
import select
import weakref

LOGGER = logging.getLogger(__name__)


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
        self.fd_to_cmd[cmd.fileno()] = weakref.ref(cmd)

        LOGGER.debug('registered %s', cmd)

    def unregister_execution(self, cmd):
        '''
        Unregister a `cmd`.

        :param Execution cmd: The cmd to unregister
        '''
        del self.fd_to_cmd[cmd.fileno()]
        self.poller.unregister(cmd)

        LOGGER.debug('unregistered %s', cmd)

    def _process_cmd_output(self, handle):
        weakcmd = self.fd_to_cmd.get(handle, None)

        cmd = weakcmd() if weakcmd else None

        if cmd:
            LOGGER.debug('%s has new output', cmd)
            cmd.process_output()

    def run(self, ms_timeout):
        '''
        Wait `ms_timeout` for some registered execution(s) to generate
        output and execute associated monitor(s).

        :param int ms_timeout: Duration waited for an event to occur
        :rtype: int
        :return: The event(s) count
        '''
        if not self.fd_to_cmd:
            return 0

        count = self.poller.poll(ms_timeout)
        for handle, __ in count:
            self._process_cmd_output(handle)

        return len(count) or -errno.ETIMEDOUT
