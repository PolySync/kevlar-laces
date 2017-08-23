#!/usr/bin/python

from behave import *

import subprocess
import shlex

def create_devel_branch(context):
	command = 'git checkout -b devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def create_random_file(context):
	command = 'echo "a not-so-random text file" >> rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def push_random_file(context):
	command = 'git add rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command2 = 'git commit -m "adding file to devel branch"'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def get_commit_hash(context):
	command = 'git reflog'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
	reflog = result.stdout.read()
	result.wait()
	log = context.reflog.splitlines()
	log0 = log[0]
	line = log0.split()
	context.commit_sha_hash = line[0]

def before_all(context):
	create_devel_branch(context)
	create_random_file(context)
	push_random_file(context)
	get_commit_hash(context)

def before_feature(context, feature):
	pass

def before_scenario(context, scenario):
	pass

def before_step(context, step):
	pass

def after_step(context, step):
	pass

def after_scenario(context, scenario):
	command = 'git reset --hard {0}'.format(context.commit_sha_hash)
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def after_feature(context, feature):
	pass

def after_all(context):
	command = 'git reset --hard 1187384'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()