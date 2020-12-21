#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from conf import settings

class BasePlugin(object):

    def __init__(self,hostname=""):
        self.mode_list = ['agent', 'salt', 'ssh']
        if hasattr(settings, 'MODE'):
            self.mode = settings.MODE
        else:
            self.mode = 'agent'
        self.hostname = hostname

    def salt(self, cmd, ):
        import salt.client

        local = salt.client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def ssh(self, cmd):
        import paramiko

        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

    def agent(self, cmd):
        import os

        output = os.popen(cmd).read()
        return output

    def exec_shell_cmd(self, cmd):
        if self.mode not in self.mode_list:
            raise Exception("settings.mode must be one of ['agent', 'salt', 'ssh']")
        func = getattr(self, self.mode)
        output = func(cmd)
        return output

    def chkos(self):
        '''
        判斷作業系統
        :return:
        '''

        os = platform.system()
        return os


    def execute(self):

        os = self.chkos()
        # print("os",os)

        if os == "Windows":
            import win32com
            import wmi
            self.wmi_obj = wmi.WMI()
            self.wmi_service_obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            self.wmi_service_connector = self.wmi_service_obj.ConnectServer(".", "root\cimv2")

            return self.windows()

        elif os == "Linux":
            # print("Linux")
            return self.linux()

        elif os == 'Darwin':
            return self.mac()


    def windows(self):
        pass


    def linux(self):
        pass


    def mac(self):
        return '暫不支持'

