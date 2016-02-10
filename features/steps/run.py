from behave import *

from yassh import *


@step(u'a command "{command}" is run as "{name}"')
def step_impl(context, command, name):
    context.command[name] = run('localhost', 'login', command)

@step(u'the command "{name}" result code is "{result:d}"')
def step_impl(context, name, result):
    context.command.get(name).should.equal(result)

@step(u'the command "{name}" result code is not "{result:d}"')
def step_impl(context, name, result):
    context.command.get(name).should_not.equal(result)

