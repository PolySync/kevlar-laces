#!/usr/bin/python

from behave import *
from hamcrest import *

import utils

def checkout_rsl_branch(context):
    command = 'git -C {0} checkout rsl'.format(context.mock_github_dir)
    utils.run_with_project_in_path(command, context)

def most_recent_file_contents(context):
    command = 'find {0} -maxdepth 1 -type f'.format(context.mock_github_dir)
    out, err, code = utils.run_with_project_in_path(command, context)
    most_recent_filename = out.strip().split()[-1]
    content = ''
    with open(most_recent_filename, 'rb') as content_file:
        content = content_file.read()

    return content

@when('I run git-securefetch')
def step_impl(context):
    command = 'git -C {0} securefetch'.format(context.mock_developer_dir)
    utils.run_with_project_in_path(command, context)

@then('The latest RSL entry should be a fetch entry')
def step_impl(context):
    checkout_rsl_branch(context)
    assert_that(len(most_recent_file_contents(context)), equal_to(5))
