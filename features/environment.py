import os
import logging

def _setup_logging():
    logging.getLogger('yassh').setLevel(logging.DEBUG)

def _alter_path(context):
    context.old_path = os.environ.get('PATH')

    fake_ssh_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  'fakessh'))

    os.environ['PATH'] = fake_ssh_dir + os.pathsep + context.old_path

def before_all(context):
    _setup_logging()
    _alter_path(context)

def before_scenario(context, scenario):
    context.command = dict()
    context.monitors = dict()

def after_all(context):
    os.environ['PATH'] = context.old_path

