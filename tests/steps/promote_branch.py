#!/usr/bin/python

from behave import *
from hamcrest import *

import subprocess
import shlex

@given('The repo has a development branch ready to promote to master')
def step_impl(context):
    context.tag = '0.0.0'

@when('I run the git-promote command from the command line')
def step_impl(context):
	#command = 'git-promote 3.4.0-devel.101 master'
	command = "ls"
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
	context.output = result.stdout.read()
	result.wait

@then('The branch should be merged into master')
def step_impl(context):
	merged = False
	command = "git reflog"
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
	context.reflog = result.stdout.read()
	result.wait()
	log = context.reflog.splitlines()
	log0 = log[0]
	line = log0.split()
	context.sha_hash = line[0]
	if 'merge' in log0 and 'devel' in log0:
		merged = True
	assert_that(merged, True)

@then('The master branch should be tagged with the semver of the promoted branch')
def step_impl(context):
	command = "git show {0}".format(context.tag)
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
	context.tag_output = result.stdout.read()
	result.wait()
	tag_data = context.tag_output.splitlines()
	commit_hash = 0
	for line in tag_data:
		if 'commit' in line:
			commit_data = line.split()
			commit_hash = commit_data[1][:6]
	assert_that(commit_hash, equal_to(context.sha_hash))
