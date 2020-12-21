#!/usr/bin/env python

from src.scripts import client

ret = {
    'mem': [
        {'slot': 'RAM slot #0', 'product': '', 'vendor': '', 'description': 'DIMM DRAM EDO', 'serial': '', 'size': 4}
    ],
    'nic': [
        {'macaddress': '00:50:56:bf:e7:6e', 'vendor': 'VMware', 'description': 'Ethernet interface', 'netmask': '',
         'model': 'VMXNET3 Ethernet Controller', 'ipaddress': '172.16.10.215', 'name': 'ens160'}
    ],
    'disk': [
        {'slot': '/dev/sda', 'product': 'Virtual disk', 'iface': 'scsi', 'capacity': 50, 'model': 'SCSI Disk',
         'serial': '', 'manufacturer': ''}
    ],
    'cpu': [],
    'basic': {
        'product': 'VMware Virtual Platform', 'uuid': '564d2dc2-0cbf-a52a-b7da-c6f001eca23f',
        'hostname': 'jumpserver', 'os_version': 'CentOS Linux release 7.6.1810 (Core) ',
        'sn': 'VMware-56 4d 2d c2 0c bf a5 2a-b7 da c6 f0 01 ec a2 3f', 'os_platform': 'Linux',
        'os_distribution': 'Linux', 'manufacturer': 'VMware, Inc.'}
}

if __name__ == '__main__':
    client()
