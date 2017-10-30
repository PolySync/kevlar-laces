#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('the repo has prerelease tag {prerelease} to promote to {target} as {release}')
def step_impl(context, prerelease, target, release):
    context.prerelease = prerelease
    context.target = target
    context.tag = release

@given('The remote repo has a release tag {release}')
def step_impl(context, release):
    utils.shell_command('git -C {0} tag -f {1}'.format(context.mock_github_dir, release))
    out, err, rc = utils.shell_command('git -C {0} ls-remote --exit-code --tags origin {1}'.format(context.mock_developer_dir, release))
    assert_that(rc, equal_to(0))

@when('I run the git-promote command from the command line')
def step_impl(context):
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, context.target)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the git-promote command targeting {branch}')
def step_impl(context, branch):
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, branch)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run the git-promote command from the {directory} directory')
def step_impl(context, directory):
    command = 'git -C {0} promote {1} {2}'.format(context.wd, context.prerelease, context.target)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@then('the tag should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target)
    log_output, unused, rc = utils.run_with_project_in_path(command, context)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.tag))

@then('the tag should not be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target)
    log_output, unused, rc = utils.run_with_project_in_path(command, context)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, not_(contains_string(context.tag)))

@then('the master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
    command = "git -C {0} describe {1}".format(context.mock_github_dir, context.target)
    describe_output, unused, rc = utils.run_with_project_in_path(command, context)
    assert_that(describe_output, equal_to_ignoring_whitespace(context.tag))

