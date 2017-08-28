#!/usr/bin/python

from behave import *

import tempfile
import shutil

import subprocess
import shlex
import tempfile
import os
import datetime

def shell_command(command):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()

def before_all(context):
    pass

def before_feature(context, feature):
    pass

def before_scenario(context, scenario):
    context.original_working_dir = os.getcwd()
    context.mock_github_dir = tempfile.mkdtemp(prefix='kevlar')

    shell_command('cp -a {0}/fixture.git {1}/.git'.format(os.getcwd(), context.mock_github_dir))

def before_step(context, step):
    pass

def after_step(context, step):
    pass

def after_scenario(context, scenario):
    shell_command('rm -rf {0}'.format(context.mock_developer_dir))
    shell_command('rm -rf {0}'.format(context.mock_github_dir))

def after_feature(context, feature):
    pass

def after_all(context):
    pass
