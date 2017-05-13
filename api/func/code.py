import paramiko


class Code:
    def __init__(self, ip, code, port=22, user="root", passwd=None, key="/root/.ssh/id_rsa"):
        self.ip = ip
        self.code = code
        self.port = port
        self.user = user
        self.passwd = passwd
        self.key = key
        self.ssh = None

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.passwd:
            self.ssh.connect(self.ip, self.port, self.user, self.passwd)
        else:
            self.ssh.connect(self.ip, self.port, self.user, self.key)

    def sed_code(self):
        """
        res 0:成功 1: 失败
        """
        _, stdout, stderr = self.ssh.exec_command('/bin/bash -lc "sed -ri \'s@^(WXCODE=).*@\\1\\"{}\\"@\' /root/settings.py && echo 0 || echo 1"'.format(self.code))
        [res] = stdout.readlines()
        return res.rstrip("\n")
            
if __name__ == '__main__':
    code = Code("172.16.20.117", "who can sefl your", passwd="justdoit")
    code.connect()
    print(code.sed_code())
