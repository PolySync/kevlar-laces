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
    utils.shell_command('cp -a {0}/test_file.txt {1}/test_file.txt'.format(os.getcwd(), context.mock_developer_dir))

    context.pre_file = tempfile.mktemp(prefix='kevlar_file')
    md5_string = '-exec md5sum {} \;'
    md5_command = "find {0} -type f -not -path '*/\.*' {1}".format(context.mock_developer_dir, md5_string)
    with open(context.pre_file, 'w+') as out_file:
        utils.pipe_stdout_to_file(md5_command, out_file)

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
    context.post_file = tempfile.mktemp(prefix='kevlar_file')
    context.diff_file = tempfile.mktemp(prefix='kevlar_file')

    md5_string = '-exec md5sum {} \;'
    md5_command = "find {0} -type f -not -path '*/\.*' {1}".format(context.mock_developer_dir, md5_string)
    with open(context.post_file, 'w+') as out_file:
        utils.pipe_stdout_to_file(md5_command, out_file)

    diff_command = 'diff {0} {1}'.format(context.pre_file, context.post_file)
    with open(context.diff_file, 'w+') as out_file:
        utils.pipe_stdout_to_file(diff_command, out_file)

    file_size = os.path.getsize(str(context.diff_file))
    assert_that(file_size, equal_to(0))

@then('The repo should be returned to the {branch} branch when I am done')
def step_impl(context, branch):
    out, err, rc = utils.run_with_project_in_path('git -C {0} branch'.format(context.mock_developer_dir), context)
    assert_that(out, contains_string('feature'))

