#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

def shell_command(command):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()

def run_with_project_in_path(command, context):
    env = os.environ
    env['PATH'] = '{0}:{1}'.format(env['PATH'], os.getcwd())
    env['GNUPGHOME'] = '{0}/fixture.gnupghome'.format(context.gnupghome_dir)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.read() if result.stdout else None
    stderr = result.stderr.read() if result.stderr else None
    result.wait()
    return_code = result.returncode
    return (stdout, stderr, return_code)

@given('A local copy of the repo on the {branch} branch')
def step_impl(context, branch):
    context.mock_developer_dir = tempfile.mkdtemp(prefix='kevlar')
    shell_command('git -C {0} clone -q file:///{1} . -b {2}'.format(context.mock_developer_dir, context.mock_github_dir, branch))
    shell_command('git -C {0} checkout -q {1}'.format(context.mock_developer_dir, branch))
    shell_command('git -C {0} config --local user.signingkey 794267AC'.format(context.mock_developer_dir))
    shell_command('git -C {0} config --local user.name "Local Test"'.format(context.mock_developer_dir))
    shell_command('git -C {0} config --local user.email "donut-reply@polysync.io"'.format(context.mock_developer_dir))
    shell_command('git -C {0} config --local gpg.program gpg2'.format(context.mock_developer_dir))

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

    context.out, context.err, context.rc = run_with_project_in_path(command, context)


@when('I run the git-mergepr --no-prune command targeting {target}')
def step_impl(context, target):
    context.target_branch = target

    command = 'git -C {0} mergepr --no-prune {1} {2}'.format(context.mock_developer_dir, context.branch_name, target)

    run_with_project_in_path(command, context)

@when('I run the git-mergepr command with a requesting branch that does not exist')
def step_impl(context):
    context.branch_name = 'not_a_branch'
    context.target_branch = 'devel'
    command = 'git -C {0} mergepr {1} {2}'.format(context.mock_developer_dir, context.branch_name, context.target_branch)
    context.out, context.err, context.rc = run_with_project_in_path(command, context)

@then('The PR should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target_branch)

    log_output, unused, rc = run_with_project_in_path(command, context)

    fields = log_output.split()
    context.sha_hash = fields[0]

    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.branch_name))

@then('The merge commit should be signed')
def step_impl(context):
    command = "git -C {0} verify-commit {1}".format(context.mock_github_dir, context.sha_hash)
    unused, verify_output, rc = run_with_project_in_path(command, context)

    assert_that(verify_output, contains_string('Signature made'))

@then("The PR's branch should be deleted from git")
def step_impl(context):
    command = "git -C {0} checkout -q {1}".format(context.mock_github_dir, context.branch_name)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()
    assert_that(result.returncode, equal_to(1))

@then("The PR's branch should still exist")
def step_impl(context):
    command = "git -C {0} checkout -q {1}".format(context.mock_github_dir, context.branch_name)
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()
    assert_that(result.returncode, equal_to(0))
