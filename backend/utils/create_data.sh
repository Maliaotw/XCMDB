#!/bin/bash

function sync_instance() {
python3 ../cmdb/manage.py shell << EOF
import os
from assets import models
import uuid

def randomIP():
    import socket
    import struct
    import random
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


models.NetworkDevice.objects.all().delete()
models.ISP.objects.all().delete()
models.Tag.objects.all().delete()
models.IDC.objects.all().delete()


data = [
    {
        'name': 'ASUS RT-AC88U', 'model': 'RT-AC88U', 'manage_ip': randomIP(), 'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'ASUS', 'sub_asset_type': 1
    },
    {
        'name': 'Cisco WS-C2960L-24TS-LL', 'model': 'WS-C2960L-24TS-LL', 'manage_ip': randomIP(),
        'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'Cisco', 'sub_asset_type': 1
    },
    {
        'name': 'Cisco WS-C2960L-48TS-LL', 'model': 'WS-C2960L-48TS-LL', 'manage_ip': randomIP(),
        'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'Cisco', 'sub_asset_type': 1
    },
    {
        'name': 'Dell N1524-24G', 'model': 'N1524-24G', 'manage_ip': randomIP(), 'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'Dell', 'sub_asset_type': 1
    },
    {
        'name': 'DrayTek Vigor2960', 'model': 'Vigor2960', 'manage_ip': randomIP(),
        'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'DrayTek', 'sub_asset_type': 1
    },
    {
        'name': 'HPE 5130-48G', 'model': 'JG934A', 'manage_ip': randomIP(), 'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48, 'manufactory': 'HP', 'sub_asset_type': 1
    },
    {
        'name': 'HPE 5130-24G', 'model': 'JG933A', 'manage_ip': randomIP(), 'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 24, 'manufactory': 'HP', 'sub_asset_type': 1
    },
    {
        'name': 'HPE 5130-48G-PoE', 'model': 'JG941A', 'manage_ip': randomIP(),
        'sn': str(uuid.uuid4()).split('-')[-1]
        , 'port_num': 48,
        'manufactory': 'HP', 'sub_asset_type': 1
    },
    {
        'name': 'FortiGate-100D', 'model': 'FG-100D', 'manage_ip': randomIP(),
        'sn': str(uuid.uuid4()).split('-')[-1], 'port_num': 16, 'manufactory': 'FORTINET', 'sub_asset_type': 3
    },
]

for i in data:
    models.NetworkDevice.objects.create(**i)

isp_data = [
    {'name':'線路A','ip_range':'61.64.127.1/24','netmask':'255.255.255.224','geteway':'61.64.127.30'},
    {'name':'線路B','ip_range':'101.101.101.1/24','netmask':'255.255.255.224','geteway':'101.101.101.30'},
    {'name':'線路C','ip_range':'61.68.33.1/24','netmask':'255.255.255.224','geteway':'61.68.33.30'},
    {'name':'線路D','ip_range':'154.221.213.1/24','netmask':'255.255.255.224','geteway':'154.221.213.1590'},
]

for i in isp_data:
    models.ISP.objects.get_or_create(**i)


tag_data = [
    {'name':'標籤A'},
    {'name':'標籤B'},
    {'name':'標籤C'},
    {'name':'標籤D'},
    {'name':'標籤E'},
    {'name':'標籤F'},
]


for i in tag_data:
    models.Tag.objects.get_or_create(**i)


idc_data = [
    {'name':'機房A','floor':5},
    {'name':'機房B','floor':8},
    {'name':'機房C','floor':10},
    {'name':'機房D','floor':12},

]

for i in idc_data:
    models.IDC.objects.get_or_create(**i)



models.Rack.objects.all().delete()
isp_obj = models.ISP.objects.all().order_by('?').first()
idc_obj = models.IDC.objects.all().order_by('?').first()
rack_obj = models.Rack.objects.create(idc=idc_obj,name="501",height=42,max_power=1000)
rack_obj.isp.add(isp_obj)

isp_obj = models.ISP.objects.all().order_by('?').first()
idc_obj = models.IDC.objects.all().order_by('?').first()
rack_obj = models.Rack.objects.create(idc=idc_obj,name="801",height=42,max_power=1000)
rack_obj.isp.add(isp_obj)


EOF
}

sync_instance
