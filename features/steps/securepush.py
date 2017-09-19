#!/usr/bin/python

from behave import *
from hamcrest import *

import utils

@when('I run git-securepush')
def step_impl(context):
    command = 'git -C {0} securepush'.format(context.mock_developer_dir)
    utils.run_with_project_in_path(command, context)
