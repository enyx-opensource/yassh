import logging
import pexpect

from .exceptions import AlreadyStartedException

_logger = logging.getLogger(__name__)

class Command(object):
    '''
    '''

    def __init__(self, name, reactor, host, username, cmd, logfile=None):
        '''
        '''
        self.name = name
        self.reactor = reactor
        self.host = host
        self.username = username
        self.cmd = cmd
        self.ssh = None

        self.logfile = logfile

        self.monitors = {}

        _logger.debug('created command "%s" as "%s" on %s@%s',
                     name, cmd, username, host)

    def __del__(self):
        '''
        '''
        self.stop()

    def __enter__(self):
        '''
        '''
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        '''
        self.stop()
        return False

    def start(self):
        '''
        '''
        if self.started():
            raise AlreadyStartedException()

        cmd = 'ssh -l {0} -o BatchMode=yes {1} "{2}"'.format(self.username,
                                                             self.host,
                                                             self.cmd)
        self.ssh = pexpect.spawn(cmd)

        self.reactor.register_command(self)

        _logger.info('started command "%s"', self.name)

    def terminate(self):
        '''
        The process is killed but any pending monitor(s)
        can still be called (e.g. on_exit)
        '''
        if not self.started():
            return

        self.ssh.terminate()

        _logger.info('terminated command "%s"', self.name)

    def stop(self):
        '''
        The process is killed and any pending monitor is discarded.
        '''
        if not self.started():
            return

        self.reactor.unregister_command(self)
        self.ssh.close()
        self.ssh = None

        _logger.info('stopped command "%s"', self.name)

    def started(self):
        '''
        '''
        return self.ssh is not None

    def fileno(self):
        '''
        '''
        return self.ssh.fileno()

    def register_monitor(self, pattern, callback):
        '''
        '''
        self.monitors.setdefault(pattern, []).append(callback)

        _logger.debug('registered monitor "%s" on %s', pattern, self.name)

    def register_exit_monitor(self, callback):
        '''
        '''
        self.register_monitor(pexpect.EOF, callback)

    def process_output(self):
        '''
        '''
        patterns = [pexpect.TIMEOUT] + self.monitors.keys()
        index = self.ssh.expect(patterns, timeout = 0)

        if index:
            # ssh.before seems only valid when something
            # other that timeout matched.
            if self.logfile:
                self.logfile.write(self.ssh.before)

            self._invoke_callbacks(patterns[index])

    def __repr__(self):
        '''
        '''
        return 'command {0}'.format(self.name)

    def _invoke_callbacks(self, matched_pattern):
        '''
        '''
        _logger.debug('matched monitor "%s" on "%s"',
                      matched_pattern, self.name)

        for callback in self.monitors[matched_pattern]:
            callback()

