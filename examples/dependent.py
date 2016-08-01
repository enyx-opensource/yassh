import logging
from yassh import Reactor, RemoteRun, LocalRun

logging.basicConfig(level=logging.DEBUG)

r = Reactor()
c1 = RemoteRun(r, 'localhost', 'user', 'sleep 5')
c2 = LocalRun(r, 'echo ok')
c3 = RemoteRun(r, 'localhost', 'user', 'echo "finished" && sleep 1')

# Start cmd2 when cmd1 complete
def start_c2():
    c2.start()
c1.register_exit_monitor(start_c2)

# Start cmd3 when cmd2 complete
def start_c3():
    c3.start()
c2.register_monitor(u'ok', start_c3)

 # Print dummy message when c3 is near terminaison
def on_c3_finished():
    print('c3 almost finished')
c3.register_monitor(u'finished', on_c3_finished)

# Start first task
c1.start()

timeout = -1 # Infinite
while r.run(timeout) > 0:
        pass
