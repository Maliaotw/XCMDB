from .base import BasePlugin
from .linuxhelper import HardwareInfo


class DiskPlugin(BasePlugin):

    def windows(self):
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():
            item_data = {}
            iface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type'] = iface
                    break
            else:
                item_data['iface_type'] = 'unknown'
            item_data['slot'] = disk.Index
            item_data['sn'] = disk.SerialNumber.strip()
            item_data['model'] = disk.Model
            item_data['manufacturer'] = disk.Manufacturer
            item_data['capacity'] = int(disk.Size) / (1024 ** 3 )
            data.append(item_data)
        return data

    def linux(self):
        ostype = 1

        HHI = HardwareInfo(ostype)

        return HHI.Disk()
