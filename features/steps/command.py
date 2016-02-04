from behave import *
from yassh import *
import sure

@step(u'a command "{command}" is created as "{name}"')
def step_impl(context, command, name):
    c = Command(name, context.reactor,
                'localhost', 'login', command)

    context.command[name] = c

    def on_exit():
        context.command[name].stop()
        del context.command[name]

    c.register_exit_monitor(on_exit)

@step(u'the command "{name}" is started')
def step_impl(context, name):
    context.command.get(name).start()

@step(u'the command "{name}" is started when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.command.get(name).start()

    context.command.get(other).register_exit_monitor(on_exit)

@step(u'the command "{name}" is stopped when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.command.get(name).terminate()

    context.command.get(other).register_exit_monitor(on_exit)

@step(u'the command "{name}" is monitored for "{pattern}" pattern')
def step_impl(context, name, pattern):
    def on_match():
        count = context.monitors.get(pattern, 0) + 1
        context.monitors[pattern] = count

    context.command.get(name).register_monitor(pattern, on_match)

@step(u'pattern "{pattern}" has been matched "{count:d}" times')
def step_impl(context, pattern, count):
    context.monitors.get(pattern, 0).should.equal(count)

@step(u'pattern "{pattern}" hasn\'t been matched')
def step_impl(context, pattern):
    context.monitors.get(pattern, None).should.be.none

