from os import path
from behave import *
import sys

from yassh import RemoteConfiguration

@when(u'a RemoteConfiguration is instantiated for {user}@{host}:{port}')
def step_impl(context, host, user, port):
    context.remote = RemoteConfiguration(host=host, username=user, port=port)

@step(u'{prop} of remote configuration is set to {value}')
def step_impl(context, prop, value):
    if prop == 'port':
        context.remote.port = value
    elif prop == 'username':
        context.remote.username = value
    else:
        context.remote.set(prop, value)

@step(u'{prop} of remote configuration is removed')
def step_impl(context, prop):
    if prop == 'port':
        context.remote.port = None
    elif prop == 'username':
        context.remote.username = None
    else:
        context.remote.unset(prop)

@step(u'{prop} of remote configuration is {value}')
def step_impl(context, prop, value):
    if prop == 'port':
        v = context.remote.port
    elif prop == 'username':
        v = context.remote.username
    elif prop == 'host':
        v = context.remote.host
    else:
        v = context.remote.get(prop)
    if value == 'unset':
        v.should.equal(None)
    else:
        v.should.equal(value)
