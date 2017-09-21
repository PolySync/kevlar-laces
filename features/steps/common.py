from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('A local copy of the repo on the {branch} branch')
def step_impl(context, branch):
    context.mock_developer_dir = tempfile.mkdtemp(prefix='kevlar')
    utils.shell_command('git -C {0} clone -q file:///{1} . -b {2}'.format(context.mock_developer_dir, context.mock_github_dir, branch))
    utils.shell_command('git -C {0} checkout -q {1}'.format(context.mock_developer_dir, branch))
    utils.shell_command('git -C {0} config --local user.signingkey 794267AC'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local user.name "Local Test"'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local user.email "donut-reply@polysync.io"'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local gpg.program gpg2'.format(context.mock_developer_dir))

@given('The {release_tag} release tag already exists')
def step_impl(context, release_tag):
    command = 'git -C {0} tag -s {1} -m {1}'.format(context.mock_github_dir, release_tag)
    utils.run_with_project_in_path(command, context)

@given('The GPG signing key is not available')
def step_impl(context):
    command = 'git -C {0} config --local user.signingkey 00000000'.format(context.mock_developer_dir)
    utils.run_with_project_in_path(command, context)

@given('I have done some work on the repo')
def step_impl(context):
    utils.shell_command('cp -a {0}/features/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

@given('The {branch} branch contains unsigned commits')
def step_impl(context, branch):
    utils.run_with_project_in_path('git -C {0} commit --allow-empty --no-gpg-sign -m "creating an unsigned commit"'.format(context.mock_developer_dir), context)

@given('The {tag} tag is unsigned')
def step_impl(context, tag):
    utils.run_with_project_in_path('git -C {0} tag -a {1} -m {1}'.format(context.mock_developer_dir, tag), context)

@given('The {tag} tag contains unsigned commits')
def step_impl(context, tag):
    utils.run_with_project_in_path('git -C {0} commit --allow-empty --no-gpg-sign -m "creating an unsigned commit"'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} tag -s {1} -m {1}'.format(context.mock_developer_dir, tag), context)

@when('The {command} command is run with the -h flag')
def step_impl(context, command):
    cmd = 'git -C {0} {1} -h'.format(context.mock_developer_dir, command)
    out, err, rc = utils.run_with_project_in_path(cmd, context)
    context.exit_code = rc
    context.stdout = out

@then('The script should return {exit_code}')
def step_impl(context, exit_code):
    assert_that(context.rc, equal_to(int(exit_code)))

@then('The merge commit should be signed')
def step_impl(context):
    command = "git -C {0} verify-commit {1}".format(context.mock_github_dir, context.sha_hash)
    unused, verify_output, rc = utils.run_with_project_in_path(command, context)
    assert_that(verify_output, contains_string('Signature made'))

@then('The repo should be returned to the state it was in before I ran the script')
def step_impl(context):
    exists = False
    original_string = 'A working file with some text'
    with open('{0}/test_file.txt'.format(context.mock_developer_dir), 'r') as check_file:
        for line in check_file:
            if original_string in line:
                exists = True
    assert_that(exists, True)

@then('The repo should be returned to the {branch} branch when I am done')
def step_impl(context, branch):
    out, err, rc = utils.run_with_project_in_path('git -C {0} branch'.format(context.mock_developer_dir), context)
    assert_that(out, contains_string('feature'))

@then('The terminal displays usage options for the {command} command')
def step_impl(context, command):
    assert_that(context.stdout, contains_string('usage:'))

@then('The terminal prints a warning')
def step_impl(context):
    assert_that(context.out, contains_string('WARNING:'))

@then('The script exits with status 0')
def step_impl(context):
    assert_that(context.exit_code, equal_to(0))
