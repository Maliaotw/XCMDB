#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import hashlib
import requests
from src import plugins
from conf import settings


auth_list = []

class AutoBase(object):
    def __init__(self,url=settings.API_URL):
        self.api_url = url

    def auth_key(self):
        current_time = time.time()
        app_id = settings.KEY
        app_id_time = "%s|%s" % (app_id, current_time)

        m = hashlib.md5()
        m.update(app_id_time.encode('utf8'))
        authkey = m.hexdigest()
        authkey_time = "%s|%s" % (authkey, current_time)
        return authkey_time

    def get_asset(self):
        pass

    def post_asset(self, msg, callback=None):
        """
        post方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        """

        authkey = self.auth_key()

        r = requests.post(
            url=self.api_url,
            json=json.dumps(msg),
            headers={settings.AUTH_KEY_NAME: authkey}
        )

        if r.status_code == 200:
            data = r.json()
            return data['data']
        else:
            return u'Error'



    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('you must implement process method')

    def callback(self, status, response):
        """
        提交资产后的回调函数
        :param status:
        :param response:
        :return:
        """
        pass


class AutoAgent(AutoBase):

    def process(self):
        """
        获取当前资产信息

        :return:
        """
        server_info = plugins.get_server_info()
        # print(type(server_info))
        # print(server_info)
        return server_info


    def run(self):
        ret = self.process()
        # print(ret)
        return self.post_asset(ret)


class AutoSSH(AutoBase):
    pass


class AutoSalt(AutoBase):
    pass
