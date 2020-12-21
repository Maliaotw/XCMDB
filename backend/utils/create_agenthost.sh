#!/bin/bash

function sync_instance() {
python3 ../cmdb/manage.py shell << EOF

from hosts import models
import random
import uuid


def randomMAC():
    import random
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def randomIP():
    import socket
    import struct
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


def set_hostdata():
    host_list = []

    for i in ('demo', 'a6', 'r3', 'c56', 'c400', 'xmi168', 'bai334', 'ju', 'ew', 'c88', 'duuu3', 'euc2', 'xicd', 'c333', 'c67'):
        webs = random.choice((1, 2))
        for h in range(webs):
            data = {
                'hostname': '%s-web%s' % (i, h + 1),
                'uuid': str(uuid.uuid4())
            }
            host_list.append(data)

    return host_list


def get_hostdata():
    data = [
        {'hostname': 'demo-web1', 'uuid': '54d0f26c-f479-4833-aa38-69e0e78193b4'},
        {'hostname': 'a666-web1', 'uuid': '1e2bd5f6-a38f-4bf6-9670-5f4effe8ae08'},
        {'hostname': 'b888-web2', 'uuid': '754e94a0-f3be-49a7-be42-e90095414201'},
        {'hostname': 'r3-web1', 'uuid': '11f728db-de47-4cbc-a4d3-be0539e4a0ed'},
        {'hostname': 'c56-web1', 'uuid': '394bf518-6610-40d6-ac26-e45a1251576a'},
        {'hostname': 'c56-web2', 'uuid': 'b97af28a-25bf-431f-8abd-74ea841363ac'},
        {'hostname': 'c400-web1', 'uuid': '5d7b57f7-7160-44d9-b7ba-9578b470bede'},
        {'hostname': 'c400-web2', 'uuid': '7f9d8999-aae1-4f3b-9ef1-2f91325ecdc6'},
        {'hostname': 'xmi168-web1', 'uuid': 'e1178302-3312-4da2-b313-a37321470d88'},
        {'hostname': 'xmi168-web2', 'uuid': '94c7aad8-aa2d-4ee9-b91e-d4a36519d5a9'},
        {'hostname': 'bai334-web1', 'uuid': '98d0ede4-cea8-48ab-a41f-5d182892f4fd'},
        {'hostname': 'ju-web1', 'uuid': 'd9d72286-2538-43f9-86ec-8c85387b1ec0'},
        {'hostname': 'ew-web1', 'uuid': '52bd04ee-c318-492a-9c25-593d19c392d8'},
        {'hostname': 'c88-web1', 'uuid': '6baff417-b812-4a87-b798-cd8b41852840'},
        {'hostname': 'c88-web2', 'uuid': '8cfb480f-9fe2-4389-a8ae-5c254944c047'},
        {'hostname': 'duuu3-web1', 'uuid': 'ce55258f-349a-4303-95f4-18a29e955f2a'},
        {'hostname': 'euc2-web1', 'uuid': 'a393f0ea-2930-4cf3-af05-59993e00037c'},
        {'hostname': 'xicd-web1', 'uuid': '40b1aebb-a258-4853-8ba8-7270527b6379'},
        {'hostname': 'xicd-web2', 'uuid': '2429f477-8c10-47aa-82ea-0c63af6bd42c'},
        {'hostname': 'c333-web1', 'uuid': 'ec9f9bac-fb97-4150-948f-f8efbae74b58'},
        {'hostname': 'c333-web2', 'uuid': 'bb56d72a-27db-483d-bfd8-490daa5bdb1c'},
        {'hostname': 'c67-web1', 'uuid': '8e04c8aa-938b-4c15-8bff-c178fae6f1cf'},
        {'hostname': 'c67-web2', 'uuid': '63a8b466-fcc0-453d-a2d9-e189d641757d'}
    ]

    return data


def randomHost():
    import random
    host_list = []


    for i in range(10):

        r_host = random.choice(set_hostdata())

        r_mem = random.choice((1, 2))
        r_cpu = random.choice((1, 2))
        r_disk = random.choice((1, 4))
        r_nic = random.choice((1, 2))

        data = {
            'mem': [], 'nic': [], 'disk': [], 'cpu': [], 'basic': {}
        }
        for num in range(r_mem):
            data['mem'].append(
                {'slot': 'DIMM %s' % num, 'product': '', 'vendor': 'Alibaba Cloud', 'description': 'DIMM RAM',
                 'serial': '', 'size': 4})

        for num in range(r_nic):
            data['nic'].append(
                {'macaddress': randomMAC(), 'vendor': '', 'description': 'Ethernet interface', 'netmask': '',
                 'model': '', 'ipaddress': randomIP(), 'name': 'eth%s' % num})

        for num in range(r_cpu):
            data['cpu'].append({'slot': 'CPU %s' % num, 'vendor': 'Intel Corp.',
                                'cpu_model': 'Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz',
                                'version': 'pc-i440fx-2.1', 'threads': '2', 'cores': '1'})

        for num in range(r_disk):
            disk_slot = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}

            data['disk'].append(
                {'slot': '/dev/vd%s' % disk_slot[num], 'product': '', 'iface': 'virtio', 'capacity': 100,
                 'model': 'Virtual I/O device',
                 'serial': '', 'manufacturer': ''})

        data['basic'] = {
            'product': 'Alibaba Cloud ECS',
            'uuid': r_host['uuid'],
            'hostname': r_host['hostname'],
            'os_version': 'CentOS Linux release 7.6.1810 (Core) ',
            'sn': '0ed3728c-b58c-46b7-b31f-70bbd702fb87',
            'os_platform': 'Linux', 'os_distribution': 'Linux', 'manufacturer': 'Alibaba Cloud',
            'manage_ip': data['nic'][0]['ipaddress']}

        host_list.append(data)

    return host_list



def set_mem(h_obj, data):
    # models.Memory.objects.filter(slot="", manufacturer="", capacity="", host_obj="", model="", sn="")
    in_host = models.Memory.objects.filter(host_obj=h_obj)

    summary = []

    for i in data:
        if in_host.filter(slot=i['slot']):
            # 已存在 看差異
            if in_host.filter(manufacturer=i['vendor'], capacity=i['size'], slot=i['slot']):
                print("沒有變化")
                # summary.append("沒有變化")
            else:
                print("更新")
                in_host.filter(slot=i['slot']).update(manufacturer=i['vendor'], capacity=i['size'])
                summary.append("更新 %s %s" % (i['slot'], i['size']))

        else:
            print("新增內存")
            models.Memory.objects.create(manufacturer=i['vendor'], capacity=i['size'], slot=i['slot'],
                                         host_obj=h_obj,
                                         model=i['product'], sn=i['serial'])
            summary.append("新增 %s %s" % (i['slot'], i['size']))

    if summary:
        summary.insert(0, "內存:")

    return summary


def set_nic(h_obj, data):
    summary = []

    for i in data:
        # models.NIC.objects.filter(macaddress="", model="", netmask="", ipaddress="", name='')
        in_host = models.NIC.objects.filter(host_obj=h_obj)

        if in_host.filter(name=i['name']):
            # 已存在
            if in_host.filter(macaddress=i['macaddress'], ipaddress=i['ipaddress'], name=i['name']):
                print("沒有變化")
            else:
                print("更新")
                in_host.filter(name=i['name']).update(macaddress=i['macaddress'], ipaddress=i['ipaddress'],
                                                      netmask=i['netmask'], model=i['model'])
                summary.append("更新 %s %s" % (i['name'], i['ipaddress']))
        else:
            print("新增網卡")
            models.NIC.objects.create(macaddress=i['macaddress'],
                                      model=i['model'],
                                      netmask=i['netmask'],
                                      ipaddress=i['ipaddress'], name=i['name'], host_obj=h_obj)
            summary.append("新增 %s %s" % (i['name'], i['ipaddress']))

    if summary:
        summary.insert(0, "網卡:")

    return summary


def set_disk(h_obj, data):
    summary = []

    for i in data:
        # models.Disk.objects.filter(slot="", model="", capacity="", host_obj="", sn="", manufacturer="", iface_type="")
        in_host = models.Disk.objects.filter(host_obj=h_obj)

        if in_host.filter(slot=i['slot']):
            # 已存在
            if in_host.filter(capacity=i['capacity'], slot=i['slot'], model=i['model']):
                print("沒有變化")
                # summary.append("沒有變化")
            else:
                print("更新")
                in_host.filter(slot=i['slot']).update(capacity=i['capacity'], slot=i['slot'], model=i['model'],
                                                      sn=i['serial'], manufacturer=i['manufacturer'],
                                                      iface_type=i['iface'])
                summary.append("更新 %s %s" % (i['slot'], i['capacity']))
        else:
            print("新增硬盤")
            models.Disk.objects.create(slot=i['slot'], model=i['model'], capacity=i['capacity'], host_obj=h_obj,
                                       sn=i['serial'], manufacturer=i['manufacturer'], iface_type=i['iface'])
            summary.append("新增 %s %s" % (i['slot'], i['capacity']))

    if summary:
        summary.insert(0, "硬盤:")

    return summary


def set_cpu(h_obj, data):
    summary = []

    for i in data:
        # models.CPU.objects.filter(slot="",manufacturer="",model="",cores="",threads="",host_obj="")
        in_host = models.CPU.objects.filter(host_obj=h_obj)

        if in_host.filter(slot=i['slot']):
            # 已存在
            if in_host.filter(slot=i['slot'], model=i['cpu_model']):
                print("沒有變化")
            else:
                in_host.filter(slot=i['slot']).update(manufacturer=i['vendor'], model=i['cpu_model'],
                                                      cores=i['cores'],
                                                      threads=i['threads'])
                summary.append("更新 %s %s" % (i['slot'], i['cores']))
        else:
            print("新增CPU")
            models.CPU.objects.create(slot=i['slot'], manufacturer=i['vendor'], model=i['cpu_model'],
                                      cores=i['cores'],
                                      threads=i['threads'], host_obj=h_obj)
            summary.append("新增 %s %s" % (i['slot'], i['cores']))

    if summary:
        summary.insert(0, "CPU:")

    return summary


for d in randomHost():

    basic = d['basic']

    record = {'title': '', 'summary': []}

    # print(basic['hostname'])

    node = models.Node.objects.get_or_create(name="-".join(basic['hostname'].split("-")[:-1]))[0]

    h_obj = models.Host.objects.get_or_create(name=basic['hostname'], sn=basic['uuid'], node=node, cate=2)
    if h_obj[1]:
        # 新增
        print("新增", h_obj)

        h_obj = h_obj[0]
        h_obj.manage_ip = basic['manage_ip']
        h_obj.total_memory = sum([i['size'] for i in d['mem']])
        h_obj.total_disk = sum([i['capacity'] for i in d['disk']])
        h_obj.total_cores = sum([int(i['cores']) for i in d['cpu']])
        h_obj.save()

        record['title'] = '新增 %s' % h_obj.name

    else:
        # 更新
        print("更新", h_obj)
        h_obj = h_obj[0]
        h_obj.manufacturer = basic['manufacturer']
        h_obj.os_platform = basic['os_platform']
        h_obj.os_distribution = basic['os_distribution']
        h_obj.os_version = basic['os_version']
        h_obj.manage_ip = basic['manage_ip']
        h_obj.model = basic['product']
        h_obj.total_memory = sum([i['size'] for i in d['mem']])
        h_obj.total_disk = sum([i['capacity'] for i in d['disk']])
        h_obj.total_cores = sum([int(i['cores']) for i in d['cpu']])

        h_obj.save()

    record['summary'] += set_mem(h_obj, d['mem'])

    record['summary'] += set_nic(h_obj, d['nic'])

    record['summary'] += set_disk(h_obj, d['disk'])

    record['summary'] += set_cpu(h_obj, d['cpu'])

    if record['summary'] and not record['title']:
        record['title'] = '更新 %s' % h_obj.name

    if record['title']:
        # 建立資產變更紀錄表
        record['summary'] = "\n".join(record['summary'])
        models.HostRecord.objects.create(host_obj=h_obj, **record)



EOF
}

sync_instance
