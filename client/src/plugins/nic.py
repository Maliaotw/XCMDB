

from .base import BasePlugin
from .linuxhelper import HardwareInfo

class NicPlugin(BasePlugin):

    def windows(self):
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = {}
                item_data['macaddress'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ipaddress'] = nic.IPAddress[0]
                    item_data['netmask'] = nic.IPSubnet
                else:
                    item_data['ipaddress'] = ''
                    item_data['netmask'] = ''
                data.append(item_data)
        return data


    def linux(self):
        ostype = 1

        HHI = HardwareInfo(ostype)

        return HHI.Network()






