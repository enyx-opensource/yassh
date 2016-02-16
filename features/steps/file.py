from behave import *
from os import path
import io
import sure


@step(u'a "{name}" file is created')
def step_impl(context, name):
    if name.startswith(u'/'):
        p = name
    else:
        p = path.join(context.temp_directory, name)
    io.open(p, 'w+')


@step(u'the "{name}" file exists')
def step_impl(context, name):
    p = path.join(context.temp_directory, name)
    path.exists(p).should.be.ok
