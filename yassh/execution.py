import logging
import signal
import uuid
import pexpect

from .exceptions import AlreadyStartedException

LOGGER = logging.getLogger(__name__)


class Execution(object):
    '''
    This class is used to run a shell execution.
    '''

    def __init__(self, reactor, logfile):
        '''
        Create a new shell execution without starting it

        :param Reactor reactor: The reactor used to execute monitors
        :param file logfile: A file object used to log shell execution output
        '''
        self.__id = str(uuid.uuid4()).partition('-')[0]
        self.__reactor = reactor
        self.__exec = None

        self.__logfile = logfile

        self.__monitors = {}

        self.__result = None

        self.__register_finalize()

        LOGGER.debug('created "%s"', self)

    def __del__(self):
        '''
        Stop the execution uppon destruction.
        '''
        self.__finalize()

    def __enter__(self):
        '''
        Start the execution uppon context enter.
        '''
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        Stop the execution uppon context exit.
        '''
        self.__finalize()
        return False

    def __register_finalize(self):
        def _on_exit(run):
            run.__finalize()

        self.register_exit_monitor(_on_exit)

    def __finalize(self):
        if not self.started():
            return

        self.__reactor.unregister_execution(self)
        self.__exec.close()

        if self.__exec.exitstatus is not None:
            self.__result = self.__exec.exitstatus
        else:
            self.__result = self.__exec.signalstatus

        self.__exec = None

        LOGGER.debug('finalized %s (%d)', self, self.__result)

    def _start(self, cmd, args=None):
        '''
        Start the execution.
        '''
        if self.started():
            raise AlreadyStartedException()

        self.__result = None
        self.__exec = pexpect.spawnu(cmd, args or [])

        self.__reactor.register_execution(self)

        LOGGER.debug('started %s', self)

    def _terminate(self):
        '''
        The execution is killed but any pending monitor(s)
        can still be called (e.g. on_exit).
        '''
        if not self.started():
            return

        self.__exec.kill(signal.SIGTERM)

        LOGGER.debug('terminated %s', self)

    def _send_eof(self):
        '''
        The execution is killed but any pending monitor(s)
        can still be called (e.g. on_exit).
        '''
        if not self.started():
            return

        self.__exec.sendeof()

        LOGGER.debug('terminated %s', self)

    def start(self):
        '''
        Start the execution.
        '''
        raise NotImplementedError

    @property
    def result(self):
        '''
        The return code of the execution.
        '''
        return self.__result

    def started(self):
        '''
        Check if the execution is started.

        :rtype: bool
        :return: True if started, False otherwise
        '''
        return self.__exec is not None

    def fileno(self):
        '''
        Return the execution output pipe fileno.

        :rtype: int
        :return: The pipe fileno
        '''
        return self.__exec.fileno()

    def register_monitor(self, pattern, callback):
        '''
        Register a `callback` to be executed once the `pattern` has matched
        execution output.

        :param str pattern: A pattern to match
        :param callable callback: A callback to invoke
        '''
        self.__monitors.setdefault(pattern, []).append(callback)

        LOGGER.debug('registered monitor "%s" on %s',
                     self.__pattern_name(pattern), self)

    def register_exit_monitor(self, callback):
        '''
        Register `callback` to be executed once the execution has terminated.

        :param callable callback: A callback to invoke
        '''
        self.register_monitor(pexpect.EOF, callback)

    def process_output(self):
        '''
        Try to match execution output against registered monitor(s).
        '''
        patterns = [pexpect.TIMEOUT] + list(self.__monitors.keys())
        index = self.__exec.expect(patterns, timeout=0)

        if index:
            # ssh.before seems only valid when something
            # other that timeout matched.
            if self.__logfile:
                self.__logfile.write(self.__exec.before)

            self.__invoke_callbacks(patterns[index])

    def __str__(self):
        '''
        Return the string represensation of the execution.

        :rtype: str
        :return: A string represensation of the execution
        '''
        return 'execution <{0}>'.format(repr(self))

    def __repr__(self):
        '''
        Return the id of the execution.

        :rtype str:
        :return: An id
        '''
        return str(self.__id)

    def __invoke_callbacks(self, matched_pattern):
        LOGGER.debug('matched monitor "%s" on %s',
                     self.__pattern_name(matched_pattern),
                     self)

        for callback in self.__monitors[matched_pattern]:
            callback(self)

    @staticmethod
    def __pattern_name(monitor):
        if monitor is pexpect.EOF:
            return u'@eof@'
        return monitor
