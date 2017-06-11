import re
from ansible.plugins.callback import CallbackBase


class Basic(CallbackBase):
    def __init__(self, display=None):
        self.result_q = dict()
        super().__init__(display)

    def gather_result(self, res, key, value=None):
        host = res._host.name
        if value is None:
            value = res._result.get(key)
        self.result_q[host] = {}
        self.result_q[host][key] = value
         

class SupervisorResultCallback(Basic):
    def v2_runner_on_ok(self, res):
        pattern = re.compile(r'\s+')
        mid_rest = res._result.get("stdout_lines")
        if len(mid_rest) == 1 and mid_rest[0].startswith('unix:///'):
            result = mid_rest[0]
        else:
            result = [ tuple(pattern.split(i)[0:2]) for i in mid_rest]
        self.gather_result(res, "stdout", result)

#    def v2_runner_on_failed(self, res, ignore_errors=False):
#        self.gather_result(res, 'stderr')


class CronResultCallback(Basic):
    def v2_runner_on_ok(self, res):
        mid_rest = res._result.get("stdout_lines")
        if mid_rest is None:
            return

        stdout = []
        index = -1
        for item in mid_rest:
            if item.startswith('user:'):
                user = item.split(":")[1]
                stdout.append((user, []))
                index += 1
                continue
            stdout[index][1].append(item)
        self.gather_result(res, "stdout", stdout)

