import logging
from yassh import Reactor, LocalRun

logging.basicConfig(level=logging.DEBUG)

r = Reactor()
c1 = LocalRun(r, 'sleep 5')
c2 = LocalRun(r, 'echo ok')
c3 = LocalRun(r, 'echo "finished" && sleep 1')

for c in [c1, c2, c3]:
    # Raise if the process failed.
    def _raise_on_failure(run):
        if not c.result:
            raise Exception('{0} failed'.format(c))

    c.register_exit_monitor(_raise_on_failure)
    c.start()


# Infinite
timeout = -1
while r.run(timeout) > 0:
    pass
