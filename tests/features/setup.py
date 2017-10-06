#!/usr/bin/python

import os
import tempfile
import subprocess
import shlex

def shell_command(command):
    args_list = shlex.split(command)
    result = subprocess.Popen(args_list)
    result.wait()

branch = 'feature'
original_working_dir = os.getcwd()
mock_github_dir = tempfile.mkdtemp(prefix='kevlar_git')

shell_command('cp -a {0}/features/fixture.git {1}/.git'.format(os.getcwd(), mock_github_dir))

mock_developer_dir = tempfile.mkdtemp(prefix='kevlar_dev')
shell_command('git -C {0} clone -q file:///{1} . -b {2}'.format(mock_developer_dir, mock_github_dir, branch))
shell_command('git -C {0} checkout -q {1}'.format(mock_developer_dir, branch))
shell_command('git -C {0} config --local user.signingkey 794267AC'.format(mock_developer_dir))