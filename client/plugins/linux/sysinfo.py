#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, platform, re, json
import xml2json
import socket


def xmltojson(xmlstr):
    jsonstr = xml2json.xml2json(xmlstr)
    # print jsonstr
    # jsonstr = json.dumps(xmlparse, indent=1)
    import ast
    dictstr = ast.literal_eval(jsonstr)
    return dictstr


class HardwareInfo:
    def __init__(self, ostype):
        self.ostype = ostype

    def OsInfo(self):
        os_data = {}
        if self.ostype == 1:
            getosinfo = os.popen('cat /etc/redhat-release').read()
            os_data['system'] = getosinfo.strip('\n').strip('')

        if self.ostype == 0:
            getosinfo = os.popen('grep \'PRETTY_NAME\' /etc/os-release | awk -F \'=\' \'{print $NF}\'').read()
            os_data['system'] = getosinfo.strip('\n').strip('')

        return os_data

    def Cpu(self):
        '''

        :return: list
        '''
        cpu_list = []

        getcupinfo = os.popen('lshw -xml -C cpu').read()
        cpu_metadata = xmltojson(getcupinfo)

        node = cpu_metadata['list']['node']
        print node

        if type(node) is dict:

            version = node.get("version", '')
            product = node.get("product", '')
            vendor = node.get("vendor", '')
            slot = node.get("slot", '')

            if node.get("configuration"):

                cores = node['configuration']['setting'][0]['@value']
                threads = node['configuration']['setting'][2]['@value']
                # cpu_physics_core = cpu_metadata['list']['node']['@id']
            else:
                cores = 1
                threads = 1

            cpu_list.append(
                {'version': version, 'cpu_model': product, 'vendor': vendor, 'slot': slot, 'cores': cores,
                 'threads': threads})

        return cpu_list

    def Disk(self):
        '''

        :return: list
        '''
        disk_list = []

        getdiskinfo = os.popen('lshw -xml -c disk').read()
        disk_metdata = xmltojson(getdiskinfo)

        node = disk_metdata['list']['node']

        if type(node) is dict:
            disk_product = node.get('product', '')
            disk_businfo = node.get('businfo', '')
            disk_logicalname = node.get('logicalname', '')
            disk_serial = node.get('serial', '')

            disk_size = int(node['size']['#text']) / 1024 / 1024 / 1024

            disk_list.append(
                {
                    'product': disk_product,
                    'businfo': disk_businfo,
                    'logicalname': disk_logicalname,
                    'serial': disk_serial,
                    'size': disk_size,

                }
            )
        return disk_list

    def Memory(self):
        '''

        :return: list
        '''

        mem_list = []
        get_mem_info = os.popen('lshw -xml -C Memory').read()
        mem_metadata = xmltojson(get_mem_info)
        Free_slots = 0
        Total_slots = 0
        for mems in mem_metadata['list']['node']:
            if "memory" in mems['@id']:
                mem = mems
                if 'empty' in mem['description']:
                    Free_slots = Free_slots + 1
                    Total_slots = Total_slots + 1
                    continue
                else:
                    if mems.get('node'):
                        mems = mems.get('node')

                    data = {
                        'slot': mems.get('slot', ''),
                        'description': mems.get('description', ''),
                        'size': int(mems['size']['#text']) / 1024 / 1024 / 1024,
                        'product': mems.get('product', ''),
                        'vendor': mems.get('vendor', ''),
                        'serial': mems.get("serial", '')
                    }

                    mem_list.append(data)

                    # Total_slots = Total_slots + 1

        # mem_data['Free_slots'] = Free_slots
        # mem_data['Total_slots'] = Total_slots
        return mem_list

    def network_parse(self,net):
        logicalname = net.get('logicalname')
        loop = True

        if not logicalname:
            logicalname = net['node']['logicalname']
            net = net['node']

        for i in ['veth', 'ifb', 'br', 'docker']:
            if i in logicalname:
                loop = False

        ip = ''
        for i in net['configuration']['setting']:
            if i.get('@id') == 'ip':
                ip = i['@value']

        if loop:
            data = {
                'MAC': net.get('serial', ''),
                'product': net.get('product', ''),
                'vendor': net.get('vendor', ''),
                'description': net.get('description', ''),
                'logicalname': logicalname,
                'ip': ip

            }
            return data

    def Network(self):
        '''

        :return:
        {'network': [{'product': '', 'vendor': '', 'description': 'Ethernet interface', 'ip': '172.16.0.61', 'logicalname': 'eth0', 'MAC': '00:16:3e:04:87:0e'}]}
        '''
        network_list = []
        get_net_info = os.popen('lshw -xml -C network').read()
        net_metadata = xmltojson(get_net_info)
        if isinstance(net_metadata['list']['node'],list):
            for net in net_metadata['list']['node']:
                network_list.append(self.network_parse(net))

        elif isinstance(net_metadata['list']['node'],dict):
            net = net_metadata['list']['node']
            network_list.append(self.network_parse(net))

        return network_list

    def Mainboard(self):

        t = os.popen('dmidecode | grep -A 10 "System Information"').read()

        si = t.split("\n\n")[0]

        data = {
            'manufacturer': re.findall(r'Manufacturer:\ (.*)', si)[0],
            'product': re.findall(r'Product Name:\ (.*)', si)[0],
            'version': re.findall(r'Version:\ (.*)', si)[0],
            'sn': re.findall(r'Serial Number:\ (.*)', si)[0],
            'uuid': re.findall(r'UUID:\ (.*)', si)[0],
            'wakeuptype': re.findall(r'Wake-up Type:\ (.*)', si)[0],
            'skunumber': re.findall(r'SKU Number:\ (.*)', si)[0],
            'family': re.findall(r'Family:\ (.*)', si)[0]
        }


        # 取消電源
        # get_power = os.popen('lshw -xml -C power').read()

        return data


if __name__ == '__main__':
    ostype = 1

    HHI = HardwareInfo(ostype)
    HostData = {}

    hostname = socket.gethostname()

    HostData['HOST'] = dict(HHI.OsInfo().items() + HHI.Mainboard().items() + {'hostname': hostname}.items())
    HostData['CPU'] = HHI.Cpu()
    HostData['Disk'] = HHI.Disk()
    HostData['Memory'] = HHI.Memory()
    HostData['Network'] = HHI.Network()

    print HostData

    # HostHardwareInfo['%s' % hostname.strip('\n')] = HostHardwareInfo_metdata
    # print(HostHardwareInfo)
