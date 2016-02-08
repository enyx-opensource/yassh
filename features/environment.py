import os
import logging

def before_all(context):
    context.old_path = os.environ.get('PATH')

    fake_ssh_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  'fakessh'))

    os.environ['PATH'] = fake_ssh_dir + os.pathsep + context.old_path



def before_scenario(context, scenario):
    context.command = dict()
    context.monitors = dict()
    context.contexts = dict()

def after_all(context):
    os.environ['PATH'] = context.old_path

