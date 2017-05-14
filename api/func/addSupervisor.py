import os
import sys
import random
from subprocess import Popen, STDOUT, PIPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ExecuteAnsible:
    command = "/bin/bash -lc 'supervisorctl status'"

    def __init__(self, ansible_group="all_user"):
        self.ansible_group = ansible_group
        self.r_file = os.path.join("/tmp",
                          "tmp_{}.sh".format(random.randint(10000, 10000000)))

    def write_bash(self, command):
        with open(self.r_file, 'x+') as f:
            f.write("#!/bin/bash\n")
            f.write(command)
            
    def get_supervisor_host(self):
        ansible_command = r"""ansible {} -m shell -a "{}" -f 10|grep -i success""".\
                          format(self.ansible_group, self.command) + "| awk '{print $1}'"
        return ansible_command
 
    def get_supervisor_item(self, host):
        ansible_command = r"""ansible {} -m shell -a "{}" | grep -i RUNNING""".\
                          format(host, self.command) + "| awk '{print $1}'"
        return ansible_command
    
    def execute_command(self):
        print(self.get_supervisor_host())
        with Popen(["/bin/bash", "-lc", self.get_supervisor_host()], stdout=PIPE, stderr=STDOUT) as proc:
            code = proc.wait(60)
            stdout, stderr = proc.communicate()
            if code == 0:
                print(stdout, stderr)
            

if __name__ == '__main__':
    exe = ExecuteAnsible()
    exe.execute_command()
