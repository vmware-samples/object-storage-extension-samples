import paramiko
from framework import TestLog


class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = TestLog().getlog()

    def exec_cmd(self, cmd):
        self.logger.info(cmd)
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host, port=self.port,
                           username=self.username, password=self.password,
                           timeout=300)

            stdin, stdout, stderr = client.exec_command(cmd)
            stdin.write("accept\n")
            stdout = stdout.readlines()
            stderr = stderr.readlines()
            self.logger.info((stdin, stdout, stderr))
            return stdin, stdout, stderr
        except Exception as e:
            print(e)
        finally:
            client.close()

    def exec_cmds(self, cmds):
        self.logger.info(cmds)
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host, port=self.port,
                           username=self.username, password=self.password,
                           timeout=300)

            for m in cmds:
                stdin, stdout, stderr = client.exec_command(m)
                stdin.write("accept")
                stdout = stdout.readlines()
                stderr = stderr.readlines()
                self.logger.info((stdin, stderr, stdout))
            return stdin, stdout, stderr
        except Exception as e:
            print(e)
        finally:
            client.close()

    def exec_put(self, f_p):
        pass

    def exec_get(self, f_p):
        pass


if __name__ == '__main__':
    pass
