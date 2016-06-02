from behave import *
from io import StringIO
import sure


@step(u'an output buffer is created as "{name}"')
def step_impl(context, name):
    context.out_buffers[name] = StringIO()


@step(u'the output buffer "{name}" content is')
def step_impl(context, name):
    value = context.out_buffers[name].getvalue().strip()
    print(value.encode('utf-8'))
    print('--')
    print(context.text)
    value.should_not.be.different_of(context.text)
