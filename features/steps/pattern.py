from behave import *
import sure


@step(u'pattern "{pattern}" has been matched "{count:d}" times')
def step_impl(context, pattern, count):
    context.monitors.get(pattern, 0).should.equal(count)


@step(u'pattern "{pattern}" hasn\'t been matched')
def step_impl(context, pattern):
    context.monitors.get(pattern, None).should.be.none
