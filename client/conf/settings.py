#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

MODE = os.environ.get("MODE")
API_URL = f"{os.environ.get('API_URL')}/api/assetdata/"
ASSETKEY = os.environ.get("ASSETKEY")
AUTH_KEY_NAME =  os.environ.get("AUTH_KEY_NAME")

PLUGINS = {
    'disk': 'src.plugins.disk.DiskPlugin',  # ok
    'mem': 'src.plugins.mem.MemPlugin',  # ok
    'nic': 'src.plugins.nic.NicPlugin',  # ok
    'basic': 'src.plugins.basic.BasicPlugin',
    'cpu': 'src.plugins.cpu.CpuPlugin',
    'proc': 'src.plugins.proc.ProcPlugin',
    'net': 'src.plugins.netstat.NetPlugin'
}
