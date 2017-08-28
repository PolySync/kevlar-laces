#!/usr/bin/python

from behave import *

import tempfile
import shutil

import subprocess
import shlex
import os
import datetime

def shell_command(command):
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def get_unique_number():
    now = datetime.datetime.utcnow()
    number_string = now.strftime("%Y%m%d-%H%M%S.%f")
    return number_string

def setup_environment(context):
	context.original_working_dir = os.getcwd()
	context.mock_git_dir = tempfile.mkdtemp()
	shell_command('git init {0}'.format(context.mock_git_dir))
	shell_command('cp -a /home/annie/work/tmp/test_repo_fixture/. {0}'.format(context.mock_git_dir))
	context.mock_dev_dir = tempfile.mkdtemp()
	os.chdir('{0}'.format(context.mock_dev_dir))
	shell_command('git clone file://localhost{0}'.format(context.mock_git_dir))
	context.mock_git_dir_name = os.path.basename(context.mock_git_dir)
	os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
	shell_command('git fetch origin')

def teardown_environment(context):
	os.chdir(context.original_working_dir)
	shell_command('rm -rf {0}'.format(context.mock_dev_dir))
	shell_command('rm -rf {0}'.format(context.mock_git_dir))

def before_all(context):
	pass

def before_feature(context, feature):
	pass

def before_scenario(context, scenario):
	setup_environment(context)

def before_step(context, step):
	pass

def after_step(context, step):
	pass

def after_scenario(context, scenario):
	teardown_environment(context)

def after_feature(context, feature):
	pass

def after_all(context):
	pass
