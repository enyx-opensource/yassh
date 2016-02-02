import logging
import errno
import select

logger = logging.getLogger(__name__)

class Reactor(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        self.poller = select.poll()
        self.fd_to_cmd = {}

    def register_command(self, cmd):
        '''
        '''
        self.poller.register(cmd.fileno(), select.POLLIN | select.POLLPRI)
        self.fd_to_cmd[cmd.fileno()] = cmd

        logger.debug('registered command "%s"', cmd)

    def unregister_command(self, cmd):
        '''
        '''
        del self.fd_to_cmd[cmd.fileno()]
        self.poller.unregister(cmd)

        logger.debug('unregistered command "%s"', cmd)

    def __run(self, ms_timeout):
        '''
        '''
        count = self.poller.poll(ms_timeout)
        for fd, _ in count:
            cmd = self.fd_to_cmd.get(fd, None)
            if cmd:
                cmd.process_output()

        return len(count)

    def run(self, ms_timeout):
        '''
        '''
        try:
            return self.__run(ms_timeout)
        except select.error as err:
            if err[0] == errno.EINTR:
                return 0
            raise
