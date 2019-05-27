# -*- coding:utf-8  -*-
import paramiko
from tools.log import logger
from tools.tool_params import TIMEOUT

# __author__ = 'XIAHUALOU'
# __email__ = 'hualoux.xia@intel.com'


class RemoteConn:
    def __init__(self, ip, port, user, pwd):
        self.ip = ip
        self.user = user
        self.port = port
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()

    def start_session(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.user, self.pwd, timeout=TIMEOUT)

    def close_session(self):
        self.ssh.close()

    def command(self, cmd):
        if not isinstance(cmd, str):
            cmd = str(cmd)
        return self.ssh.exec_command(cmd)

    def __enter__(self, *args, **kwargs):
        logger.info('start SSH connection')
        self.start_session()
        return self

    def __exit__(self, *args, **kwargs):
        logger.info('close SSH connection')
        self.close_session()
