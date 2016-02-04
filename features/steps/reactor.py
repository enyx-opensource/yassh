from behave import *
from yassh import *

@step(u'a reactor is created')
def step_impl(context):
    context.reactor = Reactor()

@step(u'the reactor is run')
def step_impl(context):
    while context.reactor.run(5000) > 0:
        pass

@step(u'the reactor is stopped after "{name}" terminates')
def step_impl(context, name):

    def on_exit(): context.reactor.stop()

    context.command.get(name).register_exit_monitor(on_exit)

@step(u'the reactor is stopped after following commands terminate')
def step_impl(context):

    class OnExit:
        def __init__(self):
            self.count = 0

        def __call__(self):
            self.count -= 1

            if self.count == 0:
                context.reactor.stop()

    on_exit = OnExit()

    for row in context.table:
        on_exit.count += 1
        context.command.get(row['command']).register_exit_monitor(on_exit)

