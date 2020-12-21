import os
import subprocess
import re

import logging

from django.conf import settings

from vm import models
import ipaddress


class Base:
    BASE_DIR = settings.TERRAFORM_DIR
    status = False
    dhcp = True

    @property
    def hostname(self):
        hostname = self.vars.get('hostname')
        if hostname:
            return hostname
        else:
            raise Exception("no hostname")

    @property
    def path(self):
        if self.dhcp:
            logging.info('DHCP 自動發配IP')
            conf = os.path.join(self.BASE_DIR, 'conf','dhcp')
        else:
            logging.info('靜態IP')
            conf = os.path.join(self.BASE_DIR, 'conf', 'customip')


        data = {
            'base': self.BASE_DIR,
            'conf': conf,
            'files': os.path.join(settings.PROJECT_DIR, 'data','terraform'),
            'host': os.path.join(settings.PROJECT_DIR, 'data','terraform', self.hostname)
        }
        return data

    def create_host_dir(self):
        if os.path.exists(self.path['host']):
            # print("更新host目錄")
            pass
        else:
            # print("新建host目錄")
            os.mkdir(self.path['host'])


class Network:

    def get_vars(self, ip):

        for network_obj in models.NetWork.objects.all():
            if ipaddress.IPv4Address(ip) in ipaddress.ip_network(network_obj.iprange, strict=False):
                return {
                    'network': network_obj.network,
                    'gateway': network_obj.gateway
                }


class Terraform(Base, Network):

    def __init__(self, **kwargs):
        '''
        hostname='vm-test87',ipaddress='192.168.10.87'
        '''

        self.vars = kwargs
        ipaddress = self.vars.get('ipaddress')
        if ipaddress:
            net_vars = self.get_vars(ipaddress)
            self.vars.update(net_vars)

        logging.info("%s\t%s\t%s" % (self.hostname, self.__class__.__name__, kwargs))
        logging.info(self.vars)
        self.run()

    def run(self):
        pass

    def complete(self, ret):
        if 'complete' in ret:
            logging.info('%s complete ok' % self.hostname)
        else:
            logging.info('%s complete error' % self.hostname)
            logging.error(ret)
            raise Exception(f"complete 錯誤 {self.hostname} {ret}")

    def valid(self, ret):
        string = re.findall('Resources:.(.*)\.', ret)[0]
        num = re.findall('(\d+).%s' % self.valid_text, string)[0]
        if int(num) != 0:
            logging.info('%s valid ok' % self.hostname)
            return True
        else:
            logging.error('%s valid error' % self.hostname)
            raise Exception("valid 錯誤")

    def _init(self):
        os.chdir(self.path['host'])
        ret = subprocess.getoutput('terraform init')
        if "Terraform has been successfully initialized!" in ret:
            logging.info('%s terraform init' % self.hostname)
        else:
            raise Exception(f'{self.hostname} terraform init ERROR!\nret')

    def _plan(self):
        ret = subprocess.getoutput('terraform plan')
        print(ret)
        plan_string = re.findall('Plan:\S+(.*)\.', ret)[0]
        num = re.findall('(\d+).to %s' % self.valid_text, plan_string)[0]

        if int(num) != 0:
            logging.info('%s plan ok' % self.hostname)
        else:
            logging.error('%s plan error' % self.hostname)
            raise Exception("plan 錯誤")

    def _main(self):
        ret = subprocess.getoutput(self.command)
        self.complete(ret)
        self.valid(ret)
        self.status = True
