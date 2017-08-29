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

@given('The repo has prerelease tag {prerelease} to promote to {target} as {release}')
def step_impl(context, prerelease, target, release):
    context.prerelease = prerelease
    context.target = target
    context.tag = release

@when('I run the git-promote command from the command line')
def step_impl(context):
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, context.target)
    run_with_project_in_path(command)

@then('The tag should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target)
    log_output, unused = run_with_project_in_path(command)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.tag))

@then('The master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
    command = "git -C {0} describe {1}".format(context.mock_github_dir, context.target)

    describe_output, unused = run_with_project_in_path(command)
    assert_that(describe_output, equal_to_ignoring_whitespace(context.tag))
