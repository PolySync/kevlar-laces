#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('The repo has prerelease tag {prerelease} to promote to {target} as {release}')
def step_impl(context, prerelease, target, release):
    context.prerelease = prerelease
    context.target = target
    context.tag = release


@given('There is a merge conflict')
def step_impl(context):
    utils.shell_command('cp -a {0}/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

@when('I run the git-promote command from the command line')
def step_impl(context):
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, context.target)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the git-promote command targeting a branch that does not exist')
def step_impl(context):
    nonexistent_target = 'not_a_branch'
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, nonexistent_target)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@then('The tag should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target)
    log_output, unused, rc = utils.run_with_project_in_path(command, context)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.tag))

@then('The master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
    command = "git -C {0} describe {1}".format(context.mock_github_dir, context.target)

    describe_output, unused, rc = utils.run_with_project_in_path(command, context)
    assert_that(describe_output, equal_to_ignoring_whitespace(context.tag))

