import logging
from yassh import Reactor, RemoteRun, RemoteConfiguration, LocalRun

logging.basicConfig(level=logging.DEBUG)

r = Reactor()
remote = RemoteConfiguration(host='localhost', username='user')
c1 = RemoteRun(r, remote, 'sleep 5')
c2 = LocalRun(r, 'echo ok')
c3 = RemoteRun(r, remote, 'echo "finished" && sleep 1')


def start_c2():
    # Start cmd2 when cmd1 complete
    c2.start()
c1.register_exit_monitor(start_c2)


def start_c3():
    # Start cmd3 when cmd2 complete
    c3.start()
c2.register_monitor(u'ok', start_c3)


def on_c3_finished():
    # Print dummy message when c3 is near terminaison
    print('c3 almost finished')
c3.register_monitor(u'finished', on_c3_finished)


# Start first task
c1.start()


# Infinite
timeout = -1
while r.run(timeout) > 0:
        pass
