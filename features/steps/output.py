from behave import *
from io import StringIO
import sure


@step(u'an output buffer is created as "{name}"')
def step_impl(context, name):
    context.out_buffers[name] = StringIO(newline=None)


@step(u'the output buffer "{name}" content is')
def step_impl(context, name):
    value = context.out_buffers[name].getvalue().strip()
    value.should_not.be.different_of(context.text)
