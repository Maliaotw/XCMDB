from django.shortcuts import render, HttpResponse
from hosts import tasks
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from rest_framework import permissions
import pytz
import time
import hashlib

from hosts import models as hosts_models
from assets import models as assets_models
from common import models as common_models
from django.conf import settings
import logging

logger = logging.getLogger('__name__')

auth_list = []


class AssetData(APIView):
    permission_classes = (permissions.AllowAny,)
    ASSETKEY = settings.ASSETKEY

    def set_mem(self, h_obj, data):
        # models.Memory.objects.filter(slot="", manufacturer="", capacity="", host_obj="", model="", sn="")
        in_host = hosts_models.Memory.objects.filter(host_obj=h_obj)

        summary = []

        for i in data:
            if in_host.filter(slot=i['slot']):
                # 已存在 看差異
                if in_host.filter(manufacturer=i['vendor'], capacity=i['size'], slot=i['slot']):
                    logger.debug("沒有變化")
                    # summary.append("沒有變化")
                else:
                    logger.debug("更新")
                    in_host.filter(slot=i['slot']).update(manufacturer=i['vendor'], capacity=i['size'])
                    summary.append("更新 %s %s" % (i['slot'], i['size']))

            else:
                logger.debug("新增內存")
                hosts_models.Memory.objects.create(manufacturer=i['vendor'], capacity=i['size'], slot=i['slot'],
                                                   host_obj=h_obj,
                                                   model=i['product'], sn=i['serial'])
                summary.append("新增 %s %s" % (i['slot'], i['size']))

        if summary:
            summary.insert(0, "內存:")

        return summary

    def set_nic(self, h_obj, data):
        summary = []

        for i in data:
            # models.NIC.objects.filter(macaddress="", model="", netmask="", ipaddress="", name='')
            in_host = hosts_models.NIC.objects.filter(host_obj=h_obj)

            if in_host.filter(name=i['name']):
                # 已存在
                if in_host.filter(macaddress=i['macaddress'], ipaddress=i['ipaddress'], name=i['name']):
                    logger.debug("沒有變化")
                else:
                    logger.debug("更新")
                    in_host.filter(name=i['name']).update(macaddress=i['macaddress'], ipaddress=i['ipaddress'],
                                                          netmask=i['netmask'], model=i['model'])
                    summary.append("更新 %s %s" % (i['name'], i['ipaddress']))
            else:
                logger.debug("新增網卡")
                hosts_models.NIC.objects.create(macaddress=i['macaddress'],
                                                model=i['model'],
                                                netmask=i['netmask'],
                                                ipaddress=i['ipaddress'], name=i['name'], host_obj=h_obj)
                summary.append("新增 %s %s" % (i['name'], i['ipaddress']))

        if summary:
            summary.insert(0, "網卡:")

        return summary

    def set_disk(self, h_obj, data):
        summary = []

        for i in data:
            # models.Disk.objects.filter(slot="", model="", capacity="", host_obj="", sn="", manufacturer="", iface_type="")
            in_host = hosts_models.Disk.objects.filter(host_obj=h_obj)

            if in_host.filter(slot=i['slot']):
                # 已存在
                if in_host.filter(capacity=i['capacity'], slot=i['slot'], model=i['model']):
                    logger.debug("沒有變化")
                    # summary.append("沒有變化")
                else:
                    logger.debug("更新")
                    in_host.filter(slot=i['slot']).update(capacity=i['capacity'], slot=i['slot'], model=i['model'],
                                                          sn=i['serial'], manufacturer=i['manufacturer'],
                                                          iface_type=i['iface'])
                    summary.append("更新 %s %s" % (i['slot'], i['capacity']))
            else:
                logger.debug("新增硬盤")
                hosts_models.Disk.objects.create(slot=i['slot'], model=i['model'], capacity=i['capacity'],
                                                 host_obj=h_obj,
                                                 sn=i['serial'], manufacturer=i['manufacturer'], iface_type=i['iface'])
                summary.append("新增 %s %s" % (i['slot'], i['capacity']))

        if summary:
            summary.insert(0, "硬盤:")

        return summary

    def set_cpu(self, h_obj, data):
        summary = []

        for i in data:
            # models.CPU.objects.filter(slot="",manufacturer="",model="",cores="",threads="",host_obj="")
            in_host = hosts_models.CPU.objects.filter(host_obj=h_obj)

            if in_host.filter(slot=i['slot']):
                # 已存在
                if in_host.filter(slot=i['slot'], model=i['cpu_model']):
                    logger.debug("沒有變化")
                else:
                    in_host.filter(slot=i['slot']).update(manufacturer=i['vendor'], model=i['cpu_model'],
                                                          cores=i['cores'],
                                                          threads=i['threads'])
                    summary.append("更新 %s %s" % (i['slot'], i['cores']))
            else:
                logger.debug("新增CPU")
                hosts_models.CPU.objects.create(slot=i['slot'], manufacturer=i['vendor'], model=i['cpu_model'],
                                                cores=i['cores'],
                                                host_obj=h_obj)
                summary.append("新增 %s %s" % (i['slot'], i['cores']))

        if summary:
            summary.insert(0, "CPU:")

        return summary

    def run(self, data):

        basic = data['basic']

        record = {'title': '', 'summary': []}

        # logger.debug(basic['hostname'])
        # TODO 測試用
        if basic['hostname'] in ['jumpserver', 'jenkins']:
            basic['hostname'] = "%s-web1" % basic['hostname']

        node = hosts_models.Node.objects.get_or_create(name="-".join(basic['hostname'].split("-")[:-1]))[0]

        h_obj = hosts_models.Host.objects.get_or_create(name=basic['hostname'], sn=basic['uuid'], node=node, cate=2)
        if h_obj[1]:
            # 新增
            h_obj = h_obj[0]
            ret = "新增 %s" % h_obj

            h_obj.manage_ip = self.request._request.META['REMOTE_ADDR']
            h_obj.manage_ssh = basic['manage_ssh']
            h_obj.total_memory = sum([i['size'] for i in data['mem']])
            h_obj.total_disk = sum([i['capacity'] for i in data['disk']])
            h_obj.total_cores = sum([int(i['cores']) for i in data['cpu']])
            h_obj.save()

            record['title'] = 'ADD %s' % h_obj.name

        else:
            # 更新
            h_obj = h_obj[0]

            h_obj.manufacturer = basic['manufacturer']
            h_obj.os_platform = basic['os_platform']
            h_obj.os_distribution = basic['os_distribution']
            h_obj.os_version = basic['os_version']
            h_obj.manage_ip = self.request._request.META['REMOTE_ADDR']
            h_obj.manage_ssh = basic['manage_ssh']
            h_obj.model = basic['product']
            h_obj.total_memory = sum([i['size'] for i in data['mem']])
            h_obj.total_disk = sum([i['capacity'] for i in data['disk']])
            h_obj.total_cores = sum([int(i['cores']) for i in data['cpu']])

            h_obj.save()

        # proc

        proclist = data.get('proc')
        hp = hosts_models.HostProc.objects.create(host=h_obj)
        for i in proclist:
            i['create_time'] = datetime.datetime.fromtimestamp(i['create_time']).replace(tzinfo=pytz.utc)
            proc_obj = hosts_models.Process.objects.create(**i)
            hp.proc.add(proc_obj)
        hp.save()

        # net
        logger.debug(data.get('net'))
        netlist = data.get('net')
        hn = hosts_models.HostNet.objects.create(host=h_obj)
        for i in netlist:
            net_obj = hosts_models.Net.objects.create(**i)
            hn.net.add(net_obj)
        hn.save()

        record['summary'] += self.set_mem(h_obj, data['mem'])
        record['summary'] += self.set_nic(h_obj, data['nic'])
        record['summary'] += self.set_disk(h_obj, data['disk'])
        record['summary'] += self.set_cpu(h_obj, data['cpu'])

        if record['summary'] and not record['title']:
            record['title'] = '更新 %s' % h_obj.name
            ret = "Update %s" % h_obj.name

        if record['title']:
            # 建立資產變更紀錄表
            record['summary'] = "\n".join(record['summary'])
            hosts_models.HostRecord.objects.create(host_obj=h_obj, **record)
        else:
            ret = 'Noting'

        return ret

    def post(self, request):
        import ast
        # logger.debug(request.META)
        response = 500
        auth_key_time = self.request._request.META["HTTP_AUTH_KEY"]

        auth_key_client, client_ctime = auth_key_time.split("|")
        server_current_time = time.time()
        if server_current_time - 30 > float(client_ctime):
            # 太久遠

            msg = "驗證失敗"
        if auth_key_time in auth_list:
            # 已經訪問過
            msg = "你來晚了"

        # 開始驗證
        key_time = "%s|%s" % (self.ASSETKEY, client_ctime)
        m = hashlib.md5()
        m.update(bytes(key_time, encoding='utf-8'))
        authkey = m.hexdigest()

        if authkey != auth_key_client:
            msg = "授權失敗"
        else:
            response = 200

        if response != 200:
            return Response({"msg": msg})

        auth_list.append(auth_key_time)
        data = ast.literal_eval(request.data)
        ret = self.run(data)

        return Response({'data': ret})


class DashBoardView(APIView):
    permission_classes = (permissions.AllowAny,)

    def recent_seven_days(self):
        import datetime
        from django.utils import timezone
        today = timezone.now().date()
        for i in range(7):
            yield today - datetime.timedelta(days=i)

    def get_count(self):
        counts =  [
            {'title': '資產', 'icon': 'fa fa-asterisk', 'count':assets_models.Asset.objects.all().count(), 'color': '#2d8cf0'},
            {'title': '服務器', 'icon': 'fa fa-server', 'count': hosts_models.Host.objects.filter(cate=1).count(), 'color': '#ff9900'},
            {'title': '虛擬機', 'icon': 'fa fa-cloud', 'count': hosts_models.Host.objects.filter(cate=2).count(), 'color': '#19be6b'},
            {'title': '用户', 'icon': 'fa fa-user', 'count': common_models.UserProfile.objects.all().count(), 'color': '#ed3f14'}
        ]

        return counts

    def get(self, request):

        list_week_day = list(self.recent_seven_days())
        list_week_day.reverse()

        asset_data = {
            'label': [i.strftime('%Y-%m-%d') for i in list_week_day],
            'latest_data': [],
            'create_data': []

        }

        for d in list_week_day:
            asset_data['latest_data'].append(assets_models.Asset.objects.filter(latest_date__date=d).count())
            asset_data['create_data'].append(assets_models.Asset.objects.filter(create_at__date=d).count())

        asset_type = {
            'label': [],
            'data': []
        }

        for i in assets_models.Asset.device_type_choices:
            asset_type['label'].append(i[1])
            asset_type['data'].append(assets_models.Asset.objects.filter(device_type_id=i[0]).count())

        data = {
            'asset_data': asset_data,
            'count': self.get_count(),
            'asset_type': asset_type
        }

        return Response(data)


# Create your views here.
def api_refresh_asset(request):
    """
    idrac 更新硬件信息
    :param request:
    :return:
    """

    id = request.GET.get('id')
    ret = tasks.idracinfo(idrac_id=id)

    return HttpResponse('ok')
