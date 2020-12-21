from __future__ import unicode_literals

# Create your views here.
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, ErrorDetail
from authentication.models import ExpiringToken
from rest_framework.authtoken.models import Token
from hosts import models as host_models
from common.models import UserProfile

import datetime
import time
import pytz
import hashlib

from . import models
from . import serializers
from .signals import post_auth_failed, post_auth_success
import logging

logger = logging.getLogger(__name__)

auth_list = []


class AssetData(APIView):
    permission_classes = (permissions.AllowAny,)
    ck = "mdfmsijfiosdjoidfjdf"

    def set_mem(self, h_obj, data):
        # models.Memory.objects.filter(slot="", manufacturer="", capacity="", host_obj="", model="", sn="")
        in_host = host_models.Memory.objects.filter(host_obj=h_obj)

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
                host_models.Memory.objects.create(
                    manufacturer=i['vendor'], capacity=i['size'], slot=i['slot'],
                    host_obj=h_obj,
                    model=i['product'], sn=i['serial']
                )
                summary.append("新增 %s %s" % (i['slot'], i['size']))

        if summary:
            summary.insert(0, "內存:")

        return summary

    def set_nic(self, h_obj, data):
        summary = []

        for i in data:
            # models.NIC.objects.filter(macaddress="", model="", netmask="", ipaddress="", name='')
            in_host = host_models.NIC.objects.filter(host_obj=h_obj)

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
                host_models.NIC.objects.create(macaddress=i['macaddress'],
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
            in_host = host_models.Disk.objects.filter(host_obj=h_obj)

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
                host_models.Disk.objects.create(slot=i['slot'], model=i['model'], capacity=i['capacity'],
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
            in_host = host_models.CPU.objects.filter(host_obj=h_obj)

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
                host_models.CPU.objects.create(slot=i['slot'], manufacturer=i['vendor'], model=i['cpu_model'],
                                               cores=i['cores'],
                                               host_obj=h_obj)
                summary.append("新增 %s %s" % (i['slot'], i['cores']))

        if summary:
            summary.insert(0, "CPU:")

        return summary

    def run(self, data):

        basic = data['basic']

        record = {'title': '', 'summary': []}

        # print(basic['hostname'])
        # TODO 測試用
        if basic['hostname'] in ['jumpserver', 'jenkins']:
            basic['hostname'] = "%s-web1" % basic['hostname']

        node = host_models.Node.objects.get_or_create(name="-".join(basic['hostname'].split("-")[:-1]))[0]

        h_obj = host_models.Host.objects.get_or_create(name=basic['hostname'], sn=basic['uuid'], node=node, cate=2)
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
        hp = host_models.HostProc.objects.create(host=h_obj)
        for i in proclist:
            i['create_time'] = datetime.datetime.fromtimestamp(i['create_time']).replace(tzinfo=pytz.utc)
            proc_obj = host_models.Process.objects.create(**i)
            hp.proc.add(proc_obj)
        hp.save()

        # net
        print(data.get('net'))
        netlist = data.get('net')
        hn = host_models.HostNet.objects.create(host=h_obj)
        for i in netlist:
            net_obj = host_models.Net.objects.create(**i)
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
            host_models.HostRecord.objects.create(host_obj=h_obj, **record)
        else:
            ret = 'Noting'

        return ret

    def post(self, request):
        import ast
        # print(request.META)
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
        key_time = "%s|%s" % (self.ck, client_ctime)
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
        # print(request)
        # self.request
        data = ast.literal_eval(request.data)
        ret = self.run(data)

        return Response({'data': ret})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        vaild = serializer.is_valid()
        if vaild:

            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            self.send_auth_signal(success=True, user=user)

            return Response({
                'token': token.key,
                'user': user.username,
                # 'user_id': user.pk,
                # 'email': user.email
            })
        else:

            logging.debug('UserLoginView form_invalid')

            # write login failed log
            user = serializer.data['username']
            exist = UserProfile.objects.filter(username=user)

            # 如果有帳戶 為密碼錯 , 如無帳戶為帳密錯
            reason = models.UserLoginLog.REASON_PASSWORD if exist else models.UserLoginLog.REASON_NOT_EXIST

            logging.debug(reason)

            self.send_auth_signal(success=False, username=user, reason=reason)

            raise ValidationError({'non_field_errors': [ErrorDetail(string='无法使用提供的认证信息登录。', code='authorization')]})

    def send_auth_signal(self, success=True, user=None, username='', reason=''):
        if success:
            logging.debug('send_auth_signal success')
            post_auth_success.send(sender=self.__class__, user=user, request=self.request)
        else:
            logging.debug('send_auth_signal fail')
            post_auth_failed.send(
                sender=self.__class__, username=username,
                request=self.request, reason=reason
            )


class LoginFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='contains', method='filter_username')
    datetime = filters.DateTimeFromToRangeFilter(label='datetime', method='filter_datetime')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        # print(queryset)
        return queryset.filter(datetime__range=self.data.getlist('datetime[]'))

    class Meta:
        model = models.UserLoginLog
        fields = ('username', 'status', 'datetime')


class LoginListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserLoginLog.objects.all()
    serializer_class = serializers.LoginSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LoginFilter


class ObtainExpiringAuthToken(ObtainAuthToken):
    """View enabling username/password exchange for expiring token."""
    permission_classes = [permissions.AllowAny]

    model = ExpiringToken

    def post(self, request):
        """Respond to POSTed username/password with token."""
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = ExpiringToken.objects.get_or_create(
                user=user
            )
            self.send_auth_signal(success=True, user=user)

            if token.expired():
                # If the token is expired, generate a new one.
                token.delete()
                token = ExpiringToken.objects.create(
                    user=user
                )

            data = {'token': token.key, 'username': user.username}
            return Response(data)

        else:
            logging.debug('UserLoginView form_invalid')

            # write login failed log
            user = serializer.data['username']
            exist = UserProfile.objects.filter(username=user)

            # 如果有帳戶 為密碼錯 , 如無帳戶為帳密錯
            reason = models.UserLoginLog.REASON_PASSWORD if exist else models.UserLoginLog.REASON_NOT_EXIST

            logging.debug(reason)

            self.send_auth_signal(success=False, username=user, reason=reason)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def send_auth_signal(self, success=True, user=None, username='', reason=''):
        if success:
            logging.debug('send_auth_signal success')
            post_auth_success.send(sender=self.__class__, user=user, request=self.request)
        else:
            logging.debug('send_auth_signal fail')
            post_auth_failed.send(
                sender=self.__class__, username=username,
                request=self.request, reason=reason
            )
