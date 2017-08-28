#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os


@given('The repo exists')
def step_impl(context):
    pass

@given('The repo has a PR that is ready to merge')
def step_impl(context):
    context.branch_name = 'devel'

@when('I run the git-mergepr command from the command line')
def step_impl(context):
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = 'git mergepr devel master'
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.output = result.stdout.read()
    result.wait()

@when('I run the git-mergepr --no-prune command from the command line')
def step_impl(context):
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = 'git mergepr --no-prune devel master'
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.output = result.stdout.read()
    result.wait()

@then('The PR should be merged')
def step_impl(context):
    merged = False
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = "git reflog"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.reflog = result.stdout.read()
    result.wait()
    log = context.reflog.splitlines()
    log0 = log[1]
    line = log0.split()
    context.sha_hash = line[0]
    if 'merge' in log0 and context.branch_name in log0:
        merged = True
    assert_that(merged, True)

@then('The merge commit should be signed')
def step_impl(context):
    signed = False
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = "git verify-commit {0}".format(context.sha_hash)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stderr=subprocess.PIPE)
    context.verify = result.stderr.read()
    if 'Signature made' in context.verify:
        signed = True
    result.wait()
    assert_that(signed, True)

@then("The PR's branch should be deleted from git")
def step_impl(context):
    deleted = False
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = "git checkout devel"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.communicate()
    return_code = result.returncode
    assert_that(return_code, equal_to(1))

@then("The PR's branch should still exist")
def step_impl(context):
    branch_present = False
    os.chdir('{0}/{1}'.format(context.mock_dev_dir, context.mock_git_dir_name))
    command = "git checkout devel"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.communicate()
    return_code = result.returncode
    assert_that(return_code, equal_to(0))
