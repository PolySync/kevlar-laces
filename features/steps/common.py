from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

import utils

@given('a local copy of the repo on the {branch} branch')
def step_impl(context, branch):
    context.mock_developer_dir = tempfile.mkdtemp(prefix='kevlar')
    utils.shell_command('git -C {0} clone -q file:///{1} . -b {2}'.format(context.mock_developer_dir, context.mock_github_dir, branch))
    utils.shell_command('git -C {0} checkout -q {1}'.format(context.mock_developer_dir, branch))
    utils.shell_command('git -C {0} config --local user.signingkey 794267AC'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local user.name "Local Test"'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local user.email "donut-reply@polysync.io"'.format(context.mock_developer_dir))
    utils.shell_command('git -C {0} config --local gpg.program gpg2'.format(context.mock_developer_dir))

@given('I create a new {branch} branch')
def step_impl(context, branch):
    command = 'git -C {0} checkout -b {1}'.format(context.mock_developer_dir, branch)
    utils.run_with_project_in_path(command, context)

@given('the {release_tag} release tag already exists')
def step_impl(context, release_tag):
    command = 'git -C {0} tag -s {1} -m {1}'.format(context.mock_github_dir, release_tag)
    utils.run_with_project_in_path(command, context)

@given('the GPG signing key is not available')
def step_impl(context):
    command = 'git -C {0} config --local user.signingkey 00000000'.format(context.mock_developer_dir)
    utils.run_with_project_in_path(command, context)

@given('I have done some work on the repo')
def step_impl(context):
    utils.shell_command('cp -a {0}/features/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

@given('the project contains subdirectory {directory}')
def step_impl(context, directory):
    wd = '{0}/{1}'.format(context.mock_developer_dir, directory)
    utils.run_with_project_in_path('mkdir {0}/{1}'.format(context.mock_developer_dir, directory), context)
    context.wd = wd

@given('the {branch} branch contains unsigned commits')
def step_impl(context, branch):
    utils.run_with_project_in_path('git -C {0} commit --allow-empty --no-gpg-sign -m "creating an unsigned commit"'.format(context.mock_developer_dir), context)

@given('the {tag} tag is unsigned')
def step_impl(context, tag):
    utils.run_with_project_in_path('git -C {0} tag -a {1} -m {1}'.format(context.mock_developer_dir, tag), context)

@given('the {tag} tag contains unsigned commits')
def step_impl(context, tag):
    utils.run_with_project_in_path('git -C {0} commit --allow-empty --no-gpg-sign -m "creating an unsigned commit"'.format(context.mock_developer_dir), context)
    utils.run_with_project_in_path('git -C {0} tag -s {1} -m {1}'.format(context.mock_developer_dir, tag), context)

@when('the {command} command is run with the -h flag')
def step_impl(context, command):
    cmd = 'git -C {0} {1} -h'.format(context.mock_developer_dir, command)
    context.out, context.err, context.rc = utils.run_with_project_in_path(cmd, context)

@when('I run git {action} from the {directory} directory')
def step_impl(context, action, directory):
    command = 'git -C {0} {1}'.format(context.wd, action)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@when('I run git-{action}')
def step_impl(context, action):
    command = 'git -C {0} {1}'.format(context.mock_developer_dir, action)
    context.out, context.err, context.rc = utils.run_with_project_in_path(command, context)

@then('the script should return {exit_code}')
def step_impl(context, exit_code):
    assert_that(context.rc, equal_to(int(exit_code)))

@then('the merge commit should be signed')
def step_impl(context):
    command = "git -C {0} verify-commit {1}".format(context.mock_github_dir, context.sha_hash)
    unused, verify_output, rc = utils.run_with_project_in_path(command, context)
    assert_that(verify_output, contains_string('Signature made'))

@then('the repo should be returned to the state it was in before I ran the script')
def step_impl(context):
    exists = False
    original_string = 'A working file with some text'
    with open('{0}/test_file.txt'.format(context.mock_developer_dir), 'r') as check_file:
        for line in check_file:
            if original_string in line:
                exists = True
    assert_that(exists, True)

@then('the repo should be returned to the {branch} branch when I am done')
def step_impl(context, branch):
    out, err, rc = utils.run_with_project_in_path('git -C {0} branch'.format(context.mock_developer_dir), context)
    assert_that(out, contains_string(branch))

@then('the {directory} directory should exist when I am done')
def step_impl(context, directory):
    out, err, rc = utils.shell_command('ls {0}/{1}'.format(context.mock_developer_dir, directory))
    assert_that(context.rc, equal_to(0))
      

@then('the terminal displays usage options for the {command} command')
def step_impl(context, command):
    assert_that(context.out, contains_string('usage:'))

@then('the terminal prints an error')
def step_impl(context):
    assert_that(context.out, contains_string('ERROR:'))

@then('the script exits with status 0')
def step_impl(context):
    assert_that(context.rc, equal_to(0))
