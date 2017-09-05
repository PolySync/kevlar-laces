#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('The repo has a {branch} PR that is ready to merge')
def step_impl(context, branch):
    context.branch_name = branch

@when('I run the git-mergepr command targeting {target}')
def step_impl(context, target):
    if target == 'a branch that does not exist':
        context.target_branch = 'not_a_branch'
    else:
        context.target_branch = target

    command = 'git -C {0} mergepr {1} {2}'.format(context.mock_developer_dir, context.branch_name, context.target_branch)

    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)


@when('I run the git-mergepr --no-prune command targeting {target}')
def step_impl(context, target):
    context.target_branch = target

    command = 'git -C {0} mergepr --no-prune {1} {2}'.format(context.mock_developer_dir, context.branch_name, target)

    utils.run_with_project_in_path(command, context)

@when('I run the git-mergepr command with a requesting branch that does not exist')
def step_impl(context):
    context.branch_name = 'not_a_branch'
    context.target_branch = 'devel'
    command = 'git -C {0} mergepr {1} {2}'.format(context.mock_developer_dir, context.branch_name, context.target_branch)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@then('The PR should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target_branch)

    log_output, unused, rc = utils.run_with_project_in_path(command, context)

    fields = log_output.split()
    context.sha_hash = fields[0]

    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.branch_name))


@then("The {branch} branch should {existence} exist")
def step_impl(context, branch, existence):
    command = "git -C {0} checkout -q {1}".format(context.mock_github_dir, branch)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()

    if existence == 'not':
        assert_that(result.returncode, equal_to(1))
    else:
        assert_that(result.returncode, equal_to(0))

