# -*- coding:utf-8 -*-
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from conf import settings

def client():
    if settings.MODE == 'agent':
        cli = AutoAgent(url=settings.API_URL)
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')

    ret = cli.run()
    print(ret)


