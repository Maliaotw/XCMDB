from django.shortcuts import HttpResponse
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response
from vm import serializers
from django_filters import rest_framework as filters
from . import models
from dwebsocket.decorators import accept_websocket, require_websocket
from django.core.cache import cache
import json
import time
from celery.result import AsyncResult
import ipaddress
import inspect
from settings.models import Setting, settings
from . import tasks
from django_celery_beat.models import PeriodicTask
import socket
from authentication.backends.api import WithBootstrapToken
from rest_framework import generics
import logging

logger = logging.getLogger('__name__')


class ClusterModelViewSet(viewsets.ModelViewSet):
    queryset = models.Cluster.objects.all()
    serializer_class = serializers.ClusterSerializer
    pagination_class = LimitOffsetPagination

    #     def get_template(self, obj):
    #         # obj.instance.filter(hw_is_template=True).all()
    #         return InstanceListSerializer(obj.instance.filter(hw_is_template=True).all(), many=True).data

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'data': response.data}
        response.data['template'] = serializers.InstanceListSerializer(
            models.Instance.objects.filter(hw_is_template=True).all(), many=True).data

        return response

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ClusterListSerializer
        elif self.action == 'retrieve':
            return serializers.ClusterRetrieveSerializer
        elif self.action == 'update':
            return serializers.ClusterSerializer
        return serializers.ClusterSerializer


class NetWorkStaticFilter(filters.FilterSet):
    network = filters.CharFilter(label='host', method='filter_network')

    def filter_network(self, queryset, name, value):
        logger.debug(f"{queryset} {name} {value}")
        # models.NetWork.objects.filter(cluster=2)
        return queryset.filter(**{name: value})

    class Meta:
        model = models.NetWorkStatic
        fields = "__all__"


class NetworkFilter(filters.FilterSet):
    cluster = filters.CharFilter(label='host', method='filter_cluster')

    def filter_cluster(self, queryset, name, value):
        logger.debug(f"{queryset} {name} {value}")
        # models.NetWork.objects.filter(cluster=2)
        return queryset.filter(**{name: value})

    class Meta:
        model = models.NetWork
        fields = "__all__"


class DataStoreFilter(filters.FilterSet):
    host = filters.CharFilter(label='host', method='filter_host')

    def filter_host(self, queryset, name, value):
        logger.debug(f"{queryset} {name} {value}")
        return queryset.filter(**{name: value})

    class Meta:
        model = models.DataStore
        fields = "__all__"


class DataStoreModelViewSet(viewsets.ModelViewSet):
    queryset = models.DataStore.objects.all()
    serializer_class = serializers.DatastoreListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = DataStoreFilter

    def get_serializer_class(self):
        logger.debug(f'self.action {self.action}')
        if self.action == 'update':
            return serializers.DataStoreUpdateSerializer
        return serializers.DatastoreListSerializer


# NetWorkStatic
class NetWorkStaticModelViewSet(viewsets.ModelViewSet):
    queryset = models.NetWorkStatic.objects.all()
    serializer_class = serializers.NetWorkStaticListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = NetWorkStaticFilter

    def get_serializer_class(self):
        logger.debug(f'self.action {self.action}')
        if self.action == 'create':
            return serializers.NetWorkStaticSerializer
        elif self.action == 'update':
            return serializers.NetWorkStaticUpdateSerializer
        else:
            return serializers.NetWorkStaticListSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # logger.debug(type(response))
        # logger.debug(type(response.data))
        response.data['template'] = serializers.InstanceListSerializer(
            models.Instance.objects.filter(hw_is_template=True), many=True).data

        return response


# NetWork
class NetWorkModelViewSet(viewsets.ModelViewSet):
    queryset = models.NetWork.objects.all()
    serializer_class = serializers.NetWorkListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = NetworkFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.NetWorkSerializer
        elif self.action == 'update':
            return serializers.NetWorkUpdateSerializer
        else:
            return serializers.NetWorkListSerializer


class HostFilter(filters.FilterSet):
    class Meta:
        model = models.Host
        fields = "__all__"


class InstanceFilter(filters.FilterSet):
    hw_name = filters.CharFilter(lookup_expr='contains')
    ip_address = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = models.Instance
        fields = ('hw_name', 'ip_address', 'hw_power_status', 'host', 'datastore', 'network', 'cluster')


class InstanceListView(generics.ListAPIView):
    '''Jumpserver專用API
    獲取主機清單，自動新增資產
    '''
    queryset =  models.Instance.objects.all()
    serializer_class = serializers.InstanceListSerializer
    permission_classes = [WithBootstrapToken]





# Instance
class InstanceNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['hw_name']
    # authentication_classes = [MyToken]


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InstanceFilter

    @property
    def get_vcenter_data(self):
        data = {}
        setting_objs = Setting.objects.filter(name__contains="VCENTER")
        if setting_objs:
            for i in setting_objs:
                data.update({i.name.lower(): i.cleaned_value})
        else:
            data.update(
                {
                    'vcenter_user': settings.VCENTER_USER,
                    'vcenter_pass': settings.VCENTER_PASS,
                    'vcenter_server': settings.VCENTER_SERVER,

                }
            )
        return data

    def get_terraform_data(self, data, template):
        network_obj = models.NetWork.objects.get(id=data['network'])

        context = {
            'template': template,
            'hostname': data['hw_name'],
            'vcpu': data['hw_processor_count'],
            'memory': data['hw_memtotal_mb'],
            'disk_size': data['capacity'],
            'vsphere_resource_pool': "%s/Resources" % models.Cluster.objects.get(id=data['cluster']).name,
            'host': "%s" % models.Host.objects.get(id=data['host']).name,
            'datastore': models.DataStore.objects.get(id=data['datastore']).name,
            'network': network_obj.network,
        }

        context.update(self.get_vcenter_data)

        if not network_obj.dhcp:
            # TODO IP自定義 將ip變數傳給terraform 接著判斷一下
            #  指定  tasks.create
            #  觸發到 Create 或 CustomIPCreate
            if models.NetWorkStatic.objects.filter(template__hw_name=template):
                netstatic_obj = models.NetWorkStatic.objects.filter(template__hw_name=template)
            else:
                netstatic_obj = models.NetWorkStatic.objects.filter(network=network_obj)
            # netstatic_obj  = models.NetWorkStatic.objects.filter(template__hw_name=data['hw_name'])
            if netstatic_obj:
                netstatic_obj = netstatic_obj.first()

                iprange_obj = ipaddress.ip_network(netstatic_obj.lan, strict=False)
                iprange_obj = list(iprange_obj)[2:-2]
                iplist = set([i.compressed for i in iprange_obj]) - set(
                    [i.ip_address for i in network_obj.instance_set.all()])
                iplist = sorted(iplist, key=socket.inet_aton)

                ip_data = {
                    'gateway': netstatic_obj.gateway.split('/')[0],  # 192.168.10.1/24
                    'address': iplist[0],  # netstatic_obj.lan.split('/')[0]   192.168.10.32/27
                    'netmask': netstatic_obj.gateway.split('/')[1],  # 192.168.10.1/24

                }
                context.update(ip_data)
        else:
            pass

        return context

    def create(self, request, *args, **kwargs):
        '''
        創建VM實例
        '''

        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        logging.debug(f"request {request.data}")  # POST DATA
        request.data['hw_power_status'] = 'building'
        request.data['hw_is_template'] = False
        request.data['mac_address'] = ''
        request.data['task'] = ''
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        terraform_data = self.get_terraform_data(data, request.data['template'])

        # 開始創建
        logging.debug(f"serializer {serializer.data}")
        logging.debug(f"terraform_data {terraform_data}")

        # 留意debug超時
        # logger.debug(terraform_data)
        # tasks_obj = tasks.create(terraform_data)
        tasks_obj = tasks.create.delay(terraform_data)

        # 定時任務

        # 先刪除
        # from djcelery import models as djcelery_models
        # djcelery_models.PeriodicTask.objects.filter(name="創建VM資源: {}".format("jumpserver-web01")
        PeriodicTask.objects.filter(name="創建VM資源: {}".format(terraform_data['hostname'])).delete()
        # 在創建
        PeriodicTask.objects.get_or_create(
            name="創建VM資源: {}".format(terraform_data['hostname']),
            task='vm.tasks.create',
            args=(terraform_data,),
            enabled=False
        )

        obj = serializer.instance
        obj.task = tasks_obj.id
        if terraform_data.get('address'):
            obj.ip_address = terraform_data.get('address')

        obj.save()

        return Response(obj.task)

    def list(self, request, *args, **kwargs):
        '''追加前端支持filter
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        response = super().list(request, *args, **kwargs)
        response.data['network'] = serializers.NetWorkListSerializer(models.NetWork.objects.all(), many=True).data
        response.data['host'] = serializers.HostSerializer(models.Host.objects.all(), many=True).data
        response.data['datastore'] = serializers.DatastoreListSerializer(models.DataStore.objects.all(), many=True).data

        return response

    def get_serializer_class(self):
        # logger.debug(f'self.action {self.action}')
        if self.action == 'list':
            return serializers.InstanceListSerializer
        return serializers.InstanceSerializer


# Host
class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = HostFilter

    def get_serializer_class(self):
        # logger.debug(self.__class__.__name__,'get_serializer_class',self.action)

        if self.action == 'list':
            return serializers.HostListSerializer
        return serializers.HostSerializer




@accept_websocket
def echo_once(request):
    logging.debug("%s %s" % (__name__, inspect.stack()[0][3]))

    if not request.is_websocket():  # 判断是不是websocket连接
        return HttpResponse('message')
    else:
        while True:
            time.sleep(1)

            for vm in models.VM.objects.filter(is_finish=False):

                # 讀取緩存
                data = cache.get(vm.name)

                # 成功啟動 前端頁面會自動刷新
                if vm.status == 1:
                    logging.debug("創建成功 %s %s" % (vm, vm.status))
                    vm.is_finish = True
                    vm.save()
                    data.update({'check': '2/2 check pass', 'is_finish': True})
                    for i in range(5):
                        time.sleep(2)
                        logging.debug("頁面自動刷新 第%s次 %s" % (i, data))
                        request.websocket.send(json.dumps(data))

                    continue

                # data 若為空
                logging.debug("data %s" % data)
                if not data:
                    continue

                # task 若為空
                task_id = data.get('task')
                logging.debug("task %s" % task_id)

                # 獲取異步任務對象
                if not task_id:
                    vm.check = '即將銷毀...'
                    vm.is_finish = True
                    vm.status = 5
                    data.update({'check': '即將銷毀...', 'status': '構建失敗'})
                    # cache.set(vm.name, data)
                    vm.save()
                else:

                    task_obj = AsyncResult(task_id)

                    if task_obj.status == 'FAILURE' or vm.status == 5:
                        vm.check = '即將銷毀...'
                        vm.is_finish = True
                        vm.status = 5
                        data.update({'check': '即將銷毀...', 'status': '構建失敗'})
                        # cache.set(vm.name, data)
                        vm.save()

                request.websocket.send(json.dumps(data))
