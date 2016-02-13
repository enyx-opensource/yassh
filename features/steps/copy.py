from behave import *
from yassh import *
from os import path
import sure

@step(u'a "{name}" file is created')
def step_impl(context, name):
    p = path.join(context.temp_directory, name)
    open(p, 'w+')

@step(u'a copy from "{source}" file to "{destination}" file is created as "{name}"')
def step_impl(context, source, destination, name):
    c = Copy(name, context.reactor,
             'localhost', 'login',
             path.join(context.temp_directory, source),
             path.join(context.temp_directory, destination))
    context.commands[name] = c

@step(u'a copy from "{source}" file to "{destination}" file is run')
def step_impl(context, source, destination):
    copy('localhost', 'login',
         path.join(context.temp_directory, source),
         path.join(context.temp_directory, destination))

@step(u'the "{name}" file exists')
def step_impl(context, name):
    p = path.join(context.temp_directory, name)
    path.exists(p).should.be.ok

