import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    def __init__(self, display=None):
        self.result_q = dict()
        super().__init__(display)

    def gather_result(self, res, key, value=None):
        host = res._host.name
        if value is None:
            value = res._result.get(key)
        self.result_q[host] = {}
        self.result_q[host][key] = value
         
    def v2_runner_on_ok(self, res):
        result = [ i.partition(" ")[0] for i in res._result.get("stdout_lines")]
        self.gather_result(res, "stdout", result)

    def v2_runner_on_failed(self, res, ignore_errors=False):
        self.gather_result(res, 'stderr')


class PlayRun:
    Options = namedtuple('Options', [
        'connection', 'module_path', 'forks', 'become', 'become_method',
        'become_user', 'check'])

    def __init__(self, connection_type="ssh", forks=100, host_list="/etc/ansible/hosts", passwords=None):
        self.connection_type = connection_type
        self.forks = forks
        self.host_list = host_list
        self.passwords = passwords or None

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.options = self.Options(connection=self.connection_type,
                                    module_path=None,
                                    forks=forks,
                                    become=None,
                                    become_method=None,
                                    become_user=None,
                                    check=False)

        self.results_callback = ResultCallback()
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list="/etc/ansible/hosts")

        self.variable_manager.set_inventory(self.inventory)
        self.play_source = None
        self.play = None
        self.runner = None

    def run(self, action_tuple, hosts="all", task_name="Ansible Ad-hoc"):
        """
        :param action_tuple: [('shell', 'ls'), ('ping', '')]
        """
        tasks = []
        for item in action_tuple:
            assert len(item) == 2
            module, args = item
            tasks.append(dict(action=dict(module=module, args=args)))

        self.play_source = dict(
            name = task_name,
            hosts = hosts,
            gather_facts = 'no',
            tasks = tasks
          )
        self.play = Play().load(self.play_source,
                           variable_manager=self.variable_manager,
                           loader=self.loader)
        self.runner = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=self.results_callback,
          )

        try:
            self.runner.run(self.play) 
        finally:
            if self.runner:
                self.runner.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()
            return self.results_callback.result_q

if __name__ == '__main__':
    playrun = PlayRun()
    print(playrun.run([("shell", """/bin/bash -lc 'supervisorctl status'""")], hosts="all_user"))
