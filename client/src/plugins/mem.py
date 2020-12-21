

from .base import BasePlugin
from .linuxhelper import HardwareInfo

class MemPlugin(BasePlugin):

    def windows(self):
        data = []
        ram_collections = self.wmi_service_connector.ExecQuery("Select * from Win32_PhysicalMemory")
        for item in ram_collections:
            mb = int(1024 * 1024)
            ram_size = int(item.Capacity) / mb
            item_data = {
                "slot": item.DeviceLocator.strip(),
                "capacity": ram_size,
                "model": item.Caption,
                "manufacturer": item.Manufacturer,
                "sn": item.SerialNumber,
            }
            data.append(item_data)
        return data

    def linux(self):
        ostype = 1

        HHI = HardwareInfo(ostype)

        return HHI.Memory()





