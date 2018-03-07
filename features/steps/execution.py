from behave import *

import yassh


@step(u'no execution is started')
def step_impl(context):
    pass


@step(u'the execution "{name}" is started')
def step_impl(context, name):
    context.executions.get(name).start()


@step(u'the execution "{name}" is started when "{other}" terminates')
def step_impl(context, name, other):
    def _on_exit(run):
        context.executions.get(name).start()

    context.executions.get(other).register_exit_monitor(_on_exit)


@step(u'the execution "{name}" is stopped when "{other}" terminates')
def step_impl(context, name, other):
    def _on_exit(run):
        context.executions.get(name).stop()

    context.executions.get(other).register_exit_monitor(_on_exit)


@step(u'the execution "{name}" is monitored for "{pattern}" pattern')
def step_impl(context, name, pattern):
    def _on_match(run):
        count = context.monitors.get(pattern, 0) + 1
        context.monitors[pattern] = count

    context.executions.get(name).register_monitor(pattern, _on_match)


@step(u'the executions strings are different')
def step_impl(context):
    executions_strings = set()

    for execution in context.executions.values():
        execution_string = str(execution)
        executions_strings.should_not.contain(execution_string)
        executions_strings.add(execution_string)


@step(u'starting the execution "{name}" again should raise')
def step_impl(context, name):
    start = context.executions.get(name).start
    start.when.called_with().should.throw(yassh.AlreadyStartedException)


@step(u'stopping the execution "{name}" should not raise')
def step_impl(context, name):
    stop = context.executions.get(name).stop
    stop.when.called_with().should_not.throw(Exception)
