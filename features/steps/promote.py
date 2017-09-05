#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex
import os
import tempfile

def shell_command(command):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def pipe_stdout_to_file(command, out_file):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list, stdout=out_file, stderr=subprocess.PIPE)
    result.wait()

@given('The repo has prerelease tag {prerelease} to promote to {target} as {release}')
def step_impl(context, prerelease, target, release):
    context.prerelease = prerelease
    context.target = target
    context.tag = release

@given('The {release_tag} release tag already exists')
def step_impl(context, release_tag):
    command = 'git -C {0} tag -s {1} -m {1}'.format(context.mock_github_dir, release_tag)
    run_with_project_in_path(command, context)

@given('My Yubikey is not inserted')
def step_impl(context):
    command = 'git -C {0} config --local user.signingkey 00000000'.format(context.mock_developer_dir)
    run_with_project_in_path(command, context)

@given('I have done some work on the repo')
def step_impl(context):
    shell_command('cp -a {0}/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

    context.pre_file = tempfile.mktemp(prefix='kevlar_file')
    md5_string = '-exec md5sum {} \;'
    md5_command = "find {0} -type f -not -path '*/\.*' {1}".format(context.mock_developer_dir, md5_string)
    with open(context.pre_file, 'w+') as out_file:
        pipe_stdout_to_file(md5_command, out_file)

@given('There is a merge conflict')
def step_impl(context):
    shell_command('cp -a {0}/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

@when('I run the git-promote command from the command line')
def step_impl(context):
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, context.target)
    context.out, context.err, context.rc = run_with_project_in_path(command, context)

@when('I run the git-promote command targeting a branch that does not exist')
def step_impl(context):
    nonexistent_target = 'not_a_branch'
    command = 'git -C {0} promote {1} {2}'.format(context.mock_developer_dir, context.prerelease, nonexistent_target)
    context.out, context.err, context.rc = run_with_project_in_path(command, context)

@then('The tag should be merged')
def step_impl(context):
    command = "git -C {0} log --max-count=1 --parents --format=oneline {1}".format(context.mock_github_dir, context.target)
    log_output, unused, rc = run_with_project_in_path(command, context)
    fields = log_output.split()
    context.sha_hash = fields[0]
    assert_that(log_output, contains_string('Merge'))
    assert_that(log_output, contains_string(context.tag))

@then('The master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
    command = "git -C {0} describe {1}".format(context.mock_github_dir, context.target)

    describe_output, unused, rc = run_with_project_in_path(command, context)
    assert_that(describe_output, equal_to_ignoring_whitespace(context.tag))

@then('The script should fail with exit code {exit_code}')
def step_impl(context, exit_code):
    assert_that(context.rc, equal_to(int(exit_code)))

@then('The repo should be returned to the state it was in before I ran the script')
def step_impl(context):
    context.post_file = tempfile.mktemp(prefix='kevlar_file')
    context.diff_file = tempfile.mktemp(prefix='kevlar_file')

    md5_string = '-exec md5sum {} \;'
    md5_command = "find {0} -type f -not -path '*/\.*' {1}".format(context.mock_developer_dir, md5_string)
    with open(context.post_file, 'w+') as out_file:
        pipe_stdout_to_file(md5_command, out_file)

    diff_command = 'diff {0} {1}'.format(context.pre_file, context.post_file)
    with open(context.diff_file, 'w+') as out_file:
        pipe_stdout_to_file(diff_command, out_file)

    file_size = os.path.getsize(str(context.diff_file))
    assert_that(file_size, equal_to(0))
