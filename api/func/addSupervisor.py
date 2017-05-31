import os
import sys
import random
from subprocess import Popen, STDOUT, PIPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ExecuteAnsible:
    def __init__(self, ansible_group="all_user"):
        self.ansible_group = ansible_group
        self.r_file = os.path.join("/tmp",
                          "{}.sh".format(random.randint(10000, 10000000)))

    def write_bash(self, command):
        with open(self.r_file, 'x+') as f:
            f.write("#!/bin/bash\n")
            f.write(command)
            
    def get_supervisor_host(self):
        command = "/bin/bash -lc 'supervisorctl status'"
        ansible_command = r"""
            ansible {} -m shelll -a "{}" -f 10|grep -i success""".format(self.ansible_group, command) + "| awk '{print $1}'"
        print(ansible_command)

if __name__ == '__main__':
    exe = ExecuteAnsible()
    exe.get_supervisor_host()
