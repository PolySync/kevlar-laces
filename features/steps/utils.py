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
