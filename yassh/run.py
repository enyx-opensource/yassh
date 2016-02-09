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

from .command import Command
from .reactor import Reactor

_logger = logging.getLogger(__name__)

def run(host, username, cmd, logfile=None, ms_timeout=-1):
    '''
    Run ``cmd`` on ``host`` as ``username``.

    Log command output into ``logfile`` if not None.
    Wait ``ms_timeout`` for command to complete.

    Returns:
    int
        The command result code.
    '''
    r = Reactor()
    c = Command(cmd, r, host, username, cmd, logfile)

    def on_exit(): r.stop()
    c.register_exit_monitor(on_exit)

    with c:
        while r.run(ms_timeout) > 0:
            pass

    return c.result

