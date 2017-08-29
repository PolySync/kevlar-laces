#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os

def shell_command(command):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()

def run_with_project_in_path(command):
    env = os.environ
    env['PATH'] = '{0}:{1}/..'.format(env['PATH'], os.getcwd())
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.read() if result.stdout else None
    stderr = result.stderr.read() if result.stderr else None
    result.wait()
    return (stdout, stderr)

@given('The repo has a development branch ready to promote to master')
def step_impl(context):
    context.tag = '1.0.1'

@when('I run the git-promote command from the command line')
def step_impl(context):
    command = 'git -C {0} promote 1.0.1-devel.2 master'.format(context.mock_developer_dir)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.output = result.stdout.read()
    result.wait

@then('The tag should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline master".format(context.mock_github_dir)
    log_output, unused = run_with_project_in_path(command)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.tag))
    '''
    merged = False
    command = "git -C {} reflog".format(context.mock_github_dir)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.reflog = result.stdout.read()
    result.wait()
    log = context.reflog.splitlines()
    log0 = log[0]
    line = log0.split()
    context.sha_hash = line[0]
    if 'merge' in log0 and 'devel' in log0:
        merged = True
    assert_that(merged, True)
    '''

@then('The master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
    command = "git -C {0} show {1}".format(context.mock_github_dir, context.tag)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.tag_output = result.stdout.read()
    result.wait()
    tag_data = context.tag_output.splitlines()
    commit_hash = 0
    for line in tag_data:
        if 'commit' in line:
            commit_data = line.split()
            commit_hash = commit_data[1][:7]
    assert_that(commit_hash, equal_to(context.sha_hash))
