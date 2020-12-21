

from .base import BasePlugin
from .linuxhelper import HardwareInfo

class CpuPlugin(BasePlugin):

    def windows(self):
        data = {}
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0

        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores
            cpu_model = cpu.Name
        data["cpu_count"] = len(cpu_lists)
        data["cpu_model"] = cpu_model
        data["cpu_physical_count"] = cpu_core_count
        return data

    def linux(self):
        ostype = 1

        HHI = HardwareInfo(ostype)


        return HHI.Cpu()




