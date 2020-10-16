import subprocess


def run_shell_cmd(cmd):
    """
    executes a given shell command
    :param cmd: shell command
    :return: shell command return code, stdout and stderr
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = proc.communicate()
    return_code = proc.returncode
    return return_code, stdout, stderr
