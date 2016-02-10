from behave import *

from yassh import *


@step(u'a reactor is created')
def step_impl(context):
    context.reactor = Reactor()

@step(u'the reactor is run')
def step_impl(context):
    while context.reactor.run(5000) > 0:
        pass
