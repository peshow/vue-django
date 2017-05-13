from subprocess import Popen, STDOUT,Stderr


class ExecuteAnsible:
    def __init__(self, ansible_group="all_user"):
        self.ansible_group = ansible_group

    def get_supervisor_host(self):
        command = "/bin/bash -lc 'supervisorctl status'"
