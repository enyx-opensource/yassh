from behave import *
import sure


@step(u'the "{name}" result code is "{result:d}"')
def step_impl(context, name, result):
    context.results.get(name).should.equal(result)


@step(u'the "{name}" result code is not "{result:d}"')
def step_impl(context, name, result):
    context.results.get(name).should_not.equal(result)
