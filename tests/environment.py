#!/usr/bin/python

from behave import *

import subprocess
import shlex

def checkout_devel_branch(context):
	command = 'git checkout devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def create_random_file(context):
	with open('rando_file.txt', 'w+') as random_file:
		random_file.write("a not-so-random text file")

def push_random_file(context):
	command = 'git add rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git commit -m "adding file to devel branch"'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git push origin devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def remove_file(context):
	command = 'git rm rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def commit_removal(context):
	command = 'git commit -m "test tear down"'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def push_removal(context):
	command = 'git push origin devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(command)
	result.wait()

def merge_removal(context):
	command = 'git checkout master'
	args_list = shlex.split(command)
	result = subprocess.Popen(command)
	result.wait()
	command = 'git merge -S --verify-signatures --no-ff -m "test tear down" origin/devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(command)
	result.wait
	command = 'git push origin master'
	args_list = shlex.split(command)
	result = subprocess.Popen(command)
	result.wait()

def get_commit_hash(context):
	command = 'git reflog'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list, stdout=subprocess.PIPE)
	context.reflog = result.stdout.read()
	result.wait()
	log = context.reflog.splitlines()
	log0 = log[0]
	line = log0.split()
	context.commit_sha_hash = line[0]

def delete_branch_teardown(context):
	command = 'git checkout master'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git rm rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git commit -m "test tear down"'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git push origin master'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def keep_branch_teardown(context):
	command = 'git rm rando_file.txt'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git commit -m "test tear down"'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git push origin devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git checkout master'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git merge -S --verify-signatures --no-ff -m "test tear down" origin/devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git push origin master'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()

def promote_teardown(context):
	command = 'git checkout devel'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git tag --delete 0.0.0'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	command = 'git push origin :0.0.0'
	args_list = shlex.split(command)
	result = subprocess.Popen(args_list)
	result.wait()
	keep_branch_teardown(context)

def before_all(context):
	pass

def before_feature(context, feature):
	pass

def before_scenario(context, scenario):
	context.reflog=''
	context.commit_sha_hash=''
	create_random_file(context)
	checkout_devel_branch(context)
	push_random_file(context)
	#get_commit_hash(context)

def before_step(context, step):
	pass

def before_tag(context, tag):
	pass

def after_tag(context, tag):
	if tag == 'delete_branch':
		delete_branch_teardown(context)
	elif tag == 'keep_branch':
		keep_branch_teardown(context)
	elif tag == 'promote':
		promote_teardown(context)
	else:
		pass

def after_step(context, step):
	pass

def after_scenario(context, scenario):
	#command = 'git revert {0}'.format(context.commit_sha_hash)
	#args_list = shlex.split(command)
	#result = subprocess.Popen(args_list)
	#result.wait()
	#remove_file(context)
	#commit_removal(context)
	#push_removal(context)
	#merge_removal(context)
	pass

def after_feature(context, feature):
	pass

def after_all(context):
	#command = 'git revert 4cb90ef'
	#args_list = shlex.split(command)
	#result = subprocess.Popen(args_list)
	#result.wait()
	pass