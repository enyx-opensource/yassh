from behave import *
from yassh import *
import sure

class ContextHolder(object):
    '''
    '''
    def __init__(self, **kwargs):
        '''
        '''
        self.context = Context(**kwargs)
        self.context.__enter__()

    def __del__(self):
        '''
        '''
        self.context.__exit__(None, None, None)


@step(u'a context is created')
def step_impl(context):
    context.current_holder = ContextHolder(host = 'localhost',
                                           username = 'login')

@step(u'a context command "{command}" is run as "{name}"')
def step_impl(context, command, name):
    context.command[name] = Context().run(command)

@step(u'a context command "{command}" is run it raises "{message}"')
def step_impl(context, command, message):
    try:
        Context().run(command)
        raise AssertionError('Expected an exception')
    except Exception as e:
        str(e).should.contain(message)

