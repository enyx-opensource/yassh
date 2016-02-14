from os import path
from behave import *
import sys

from yassh import *

@step(u'a copy from "{source}" file to "{destination}" file is created as "{name}"')
def step_impl(context, source, destination, name):
    c = Copy(name, context.reactor,
             'localhost', 'login',
             path.join(context.temp_directory, source),
             path.join(context.temp_directory, destination),
             sys.stdout)

    def on_exit(): context.results[name] = c.result
    c.register_exit_monitor(on_exit)

    context.executions[name] = c


@step(u'"{source}" is copied to "{destination}" as "{name}"')
def step_impl(context, source, destination, name):
    context.results[name] = copy('localhost', 'login',
                                 path.join(context.temp_directory, source),
                                 path.join(context.temp_directory, destination),
                                 sys.stdout)
