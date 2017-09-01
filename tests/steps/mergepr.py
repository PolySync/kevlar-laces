#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex

@given('The repo exists')
def step_impl(context):
    pass

@given('The repo has a PR that is ready to merge')
def step_impl(context):
    context.branch_name = 'devel'

@when('I run the git-mergepr command from the command line')
def step_impl(context):
    command = 'git-mergepr devel master'
    #command = "ls"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.output = result.stdout.read()
    result.wait()

@when('I run the git-mergepr --no-prune command from the command line')
def step_impl(context):
    command = 'git-mergepr --no-prune devel master'
    #command = "ls"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.output = result.stdout.read()
    result.wait()

@then('The PR should be merged')
def step_impl(context):
    merged = False
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
    command = "git branch"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.branch_list = result.stdout.read()
    if not context.branch_name in context.branch_list:
        deleted = True
    assert_that(deleted, True)

@then("The PR's branch should still exist")
def step_impl(context):
    branch_present = False
    command = "git branch"
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    context.branch_list = result.stdout.read()
    if context.branch_name in context.branch_list:
        branch_present = True
    assert_that(branch_present, True)