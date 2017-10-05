#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('the repo has a {branch} PR that is ready to merge')
def step_impl(context, branch):
    context.branch_name = branch

@given('there is a merge conflict')
def step_impl(context):
    branch, err, rc = utils.run_with_project_in_path('git -C {0} symbolic-ref --short HEAD'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} checkout -q devel'.format(context.mock_developer_dir), context)
    utils.shell_command('cp -a {0}/features/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))
    utils.run_with_project_in_path('git -C {0} add test_file.txt'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} commit -m "creating a merge conflict in devel"'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} push origin devel'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} checkout feature'.format(context.mock_developer_dir), context)
    utils.shell_command('cp -a {0}/features/test_file2.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))
    utils.run_with_project_in_path('git -C {0} add test_file.txt'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} commit -m "a merge conflict from feature"'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} push origin feature'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} checkout -q {1}'.format(context.mock_developer_dir, branch), context)

@given('the feature branch does not exist remotely')
def step_impl(context):
    utils.run_with_project_in_path('git -C {0} push origin :feature'.format(context.mock_developer_dir), context)

@when('I run the git-merge-pr command targeting {target}')
def step_impl(context, target):
    context.target_branch = target
    command = 'git -C {0} merge-pr {1} {2}'.format(context.mock_developer_dir, context.branch_name, context.target_branch)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the git-merge-pr --no-prune command targeting {target}')
def step_impl(context, target):
    context.target_branch = target
    command = 'git -C {0} merge-pr --no-prune {1} {2}'.format(context.mock_developer_dir, context.branch_name, target)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the git-merge-pr command with a branch to be merged that does not exist')
def step_impl(context):
    context.branch_name = 'not_a_branch'
    context.target_branch = 'devel'
    command = 'git -C {0} merge-pr {1} {2}'.format(context.mock_developer_dir, context.branch_name, context.target_branch)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the merge-pr command with the --no-prune option in position {position} targeting devel')
def step_impl(context, position):
    context.target_branch = 'devel'
    args = [context.branch_name, context.target_branch]
    args.insert(int(position), '--no-prune')
    command = 'git -C {0} merge-pr {1} {2} {3}'.format(context.mock_developer_dir, args[0], args[1], args[2])
    utils.run_with_project_in_path(command, context)

@then('the PR should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target_branch)
    log_output, unused, rc = utils.run_with_project_in_path(command, context)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.branch_name))

@then("the {branch} branch should {existence} exist")
def step_impl(context, branch, existence):
    command = "git -C {0} checkout -q {1}".format(context.mock_github_dir, branch)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()
    if existence == 'not':
        assert_that(result.returncode, equal_to(1))
    else:
        assert_that(result.returncode, equal_to(0))
