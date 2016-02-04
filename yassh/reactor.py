'''
The MIT License (MIT)

Copyright (c) 2016 EnyxSA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import logging
import errno
import select

_logger = logging.getLogger(__name__)

class Reactor(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        self.poller = select.poll()
        self.fd_to_cmd = {}
        self.stopped = False

    def stop(self):
        '''
        '''
        self.stopped = True

    def register_command(self, cmd):
        '''
        '''
        self.poller.register(cmd.fileno(), select.POLLIN | select.POLLPRI)
        self.fd_to_cmd[cmd.fileno()] = cmd

        _logger.debug('registered command "%s"', cmd)

    def unregister_command(self, cmd):
        '''
        '''
        del self.fd_to_cmd[cmd.fileno()]
        self.poller.unregister(cmd)

        _logger.debug('unregistered command "%s"', cmd)

    def _run(self, ms_timeout):
        '''
        '''
        if self.stopped:
            return 0

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
            return self._run(ms_timeout)
        except select.error as err:
            if err[0] == errno.EINTR:
                return 0
            raise
