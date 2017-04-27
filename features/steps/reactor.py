from behave import *
import sure

from yassh import Reactor


@step(u'a reactor is created')
def step_impl(context):
    context.reactor = Reactor()


@step(u'the reactor is run')
def step_impl(context):
    while True:
        count = context.reactor.run(5000)
        if count <= 0:
            break

    count.should.be.equal(0)
