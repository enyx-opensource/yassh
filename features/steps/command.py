from behave import *
from io import StringIO
import sure

from yassh import *

@step(u'a command "{command}" is created as "{name}"')
def create_command(context, command, name, logfile = None):
    c = Command(name, context.reactor,
                'localhost', 'login', command,
                logfile = logfile)

    def on_exit(): del context.commands[name]

    c.register_exit_monitor(on_exit)

    context.commands[name] = c

@step(u'a logged command "{command}" is created as "{name}"')
def create_logged_commmand(context, command, name):
    context.out_buffer = StringIO()
    create_command(context, command, name, context.out_buffer)

@step(u'the logged content is')
def step_impl(context):
    context.out_buffer.getvalue().strip().should_not.be.different_of(context.text)

@step(u'the command "{name}" is started')
def step_impl(context, name):
    context.commands.get(name).start()

@step(u'the command "{name}" is started when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.commands.get(name).start()

    context.commands.get(other).register_exit_monitor(on_exit)

@step(u'the command "{name}" is stopped when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.commands.get(name).stop()

    context.commands.get(other).register_exit_monitor(on_exit)

@step(u'the command "{name}" is monitored for "{pattern}" pattern')
def step_impl(context, name, pattern):
    def on_match():
        count = context.monitors.get(pattern, 0) + 1
        context.monitors[pattern] = count

    context.commands.get(name).register_monitor(pattern, on_match)

@step(u'pattern "{pattern}" has been matched "{count:d}" times')
def step_impl(context, pattern, count):
    context.monitors.get(pattern, 0).should.equal(count)

@step(u'pattern "{pattern}" hasn\'t been matched')
def step_impl(context, pattern):
    context.monitors.get(pattern, None).should.be.none

@step(u'the command "{name}" result code is "{result:d}"')
def step_impl(context, name, result):
    context.commands.get(name).should.equal(result)

@step(u'the command "{name}" result code is not "{result:d}"')
def step_impl(context, name, result):
    context.commands.get(name).should_not.equal(result)

