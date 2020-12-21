#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BasePlugin
import platform
import socket
from .linuxhelper import HardwareInfo
import os
import re

class BasicPlugin(BasePlugin):

    def os_platform(self):
        """
        获取系统平台
        :return:
        """
        return platform.system()

    def os_hostname(self):
        """
        獲取電腦名稱
        :return:
        """
        hostname = socket.gethostname()
        return hostname

    def windows(self):
        import win32com
        import wmi
        wmi_obj = wmi.WMI()
        # wmi_service_obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        # wmi_service_connector = self.wmi_service_obj.ConnectServer(".", "root\cimv2")

        computer_info = wmi_obj.Win32_ComputerSystem()[0]
        system_info = wmi_obj.Win32_OperatingSystem()[0]
        data = {}
        data['manufacturer'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        # data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        data['hostname'] = socket.gethostname()
        data['os_platform'] = platform.system()
        data['os_version'] = "%s %s %s %s" % (
            platform.system(), platform.release(), platform.architecture()[0], platform.version())
        data['os_distribution'] = 'Microsoft'

        return data

    def linux(self):
        ostype = 1

        HHI = HardwareInfo(ostype)

        hostname = socket.gethostname()

        os_platform = platform.system()


        updata = {'hostname': hostname, 'os_platform': os_platform, 'os_distribution': "Linux"}
        # HostData = dict(HHI.OsInfo().items() + HHI.Mainboard().items() + updata.items())
        HostData = {}
        HostData.update(HHI.OsInfo())
        HostData.update(HHI.Mainboard())
        HostData.update(updata)


        return HostData

