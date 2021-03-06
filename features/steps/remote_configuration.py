from behave import *
import sys

from yassh import RemoteConfiguration

@step(u'a RemoteConfiguration is instantiated for "{user}@{host}:{port}"')
def step_impl(context, host, user, port):
    context.remote = RemoteConfiguration(host=host, username=user, port=port)

@step(u'"{prop}" of remote configuration is set to "{value}"')
def step_impl(context, prop, value):
    if prop == 'port':
        context.remote.port = value
    elif prop == 'username':
        context.remote.username = value
    else:
        context.remote.set(prop, value)

@step(u'"{prop}" of remote configuration is removed')
def step_impl(context, prop):
    if prop == 'port':
        context.remote.port = None
    elif prop == 'username':
        context.remote.username = None
    else:
        context.remote.unset(prop)

@step(u'"{prop}" of remote configuration is "{value}"')
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

@step(u'remote configuration __repr__() contains port "{port}" and user "{user}"')
def step_impl(context, port, user):
    expected = str([
        u'-o', u'Port={0}'.format(port),
        u'-o', u'User={0}'.format(user)
    ])
    context.remote.__repr__().should.equal(expected)
