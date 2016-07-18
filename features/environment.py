from tempfile import mkdtemp
import os
import shutil
import logging


def before_all(context):
    context.old_path = os.environ.get('PATH')

    fake_ssh_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   'fakessh'))

    os.environ['PATH'] = fake_ssh_dir + os.pathsep + context.old_path


def before_scenario(context, scenario):
    context.temp_directory = mkdtemp()
    context.executions = dict()
    context.monitors = dict()
    context.results = dict()
    context.out_buffers = dict()


def after_scenario(context, scenario):
    shutil.rmtree(context.temp_directory)


def after_all(context):
    os.environ['PATH'] = context.old_path
