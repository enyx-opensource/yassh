from behave import *
import sure

from yassh import *


@step(u'the execution "{name}" is started')
def step_impl(context, name):
    context.executions.get(name).start()


@step(u'the execution "{name}" is started when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.executions.get(name).start()

    context.executions.get(other).register_exit_monitor(on_exit)


@step(u'the execution "{name}" is stopped when "{other}" terminates')
def step_impl(context, name, other):
    def on_exit():
        context.executions.get(name).stop()

    context.executions.get(other).register_exit_monitor(on_exit)


@step(u'the execution "{name}" is monitored for "{pattern}" pattern')
def step_impl(context, name, pattern):
    def on_match():
        count = context.monitors.get(pattern, 0) + 1
        context.monitors[pattern] = count

    context.executions.get(name).register_monitor(pattern, on_match)
