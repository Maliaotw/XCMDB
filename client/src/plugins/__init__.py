# -*- coding:utf-8 -*-
from src.plugins.basic import BasicPlugin
from conf import settings
import importlib


def get_server_info(hostname=None):
    """
    获取服务器基本信息
    :param hostname: agent模式时，hostname为空；salt或ssh模式时，hostname表示要连接的远程服务器
    :return:
    """
    response = {}
    for k, v in settings.PLUGINS.items():
        module_path, cls_name = v.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), cls_name)
        obj = cls(hostname).execute()
        response[k] = obj

    return response
