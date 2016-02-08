from behave import *
from yassh import *
import sure

@step(u'a context "{name}" is created')
def step_impl(context, name):
    context.contexts[name] = Context(host='localhost', username='login')

@step(u'the context "{name}" is entered')
def step_impl(context, name):
    context.contexts[name].__enter__()

@step(u'the context "{name}" is exited')
def step_impl(context, name):
    context.contexts[name].__exit__(None, None, None)

@step(u'a context "{ctx_name}" command "{command}" is run as "{name}"')
def step_impl(context, ctx_name, command, name):
    context.command[name] = context.contexts[ctx_name].run(command)

@step(u'a context "{ctx_name}" command "{command}" is run it raises "{message}"')
def step_impl(context, ctx_name, command, message):
    try:
        context.contexts[ctx_name].run(command)
        raise AssertionError('Expected an exception')
    except Exception as e:
        str(e).should.contain(message)

