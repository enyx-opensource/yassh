import logging
from yassh import Reactor, RemoteRun, LocalRun

logging.basicConfig(level=logging.DEBUG)

r = Reactor()
c1 = LocalRun(r, 'sleep 5')
c2 = LocalRun(r, 'echo ok')
c3 = LocalRun(r, 'echo "finished" && sleep 1')

for c in [c1, c2, c3]:
    # Raise if the process failed.
    def raise_on_failure():
        if not c.result:
            raise Exception('{0} failed'.format(c))

    c.register_exit_monitor(raise_on_failure)
    c.start()

timeout = -1 # Infinite
while r.run(timeout) > 0:
    pass
