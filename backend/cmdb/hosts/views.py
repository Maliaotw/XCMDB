from django.shortcuts import render, HttpResponse

# 引入drf功能模塊

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response

# model
from hosts import models
from assets import models as assets_models
# 引入序列化
from hosts import serializers

from django_filters import rest_framework as filters

import inspect
import logging

import django_filters


# BusUnit
class BusUnitModelViewSet(viewsets.ModelViewSet):
    '''
    BusUnit 序列化
    '''
    queryset = models.BusinessUnit.objects.all()
    serializer_class = serializers.BusUnitListSerializer
    pagination_class = LimitOffsetPagination


# Host
class HostFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    node = filters.CharFilter(method="filter_node")

    def filter_node(self, queryset, name, value):
        return queryset.filter(node__name=value)


    class Meta:
        model = models.Host
        fields = ('name', 'enabled')


class HostModelViewSet(viewsets.ModelViewSet):
    '''
    Host 序列化
    '''

    queryset = models.Host.objects.filter(cate=2)
    serializer_class = serializers.HostListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = HostFilter

    def get_serializer_class(self):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))

        if self.action == 'list':
            return serializers.HostListSerializer
        return serializers.HostSerializer

    def get_object(self):
        obj = super().get_object()
        # 啟用入資產
        # if not obj.asset.all():
        #     assets_models.Asset.objects.create(content_object=obj, name=obj.name, device_type_id=1)
        obj.enabled = True
        obj.save()
        return obj

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['node'] = serializers.NodeListSerializer(models.Node.objects.all(),many=True).data
        return response



# Instance
class InstanceModelViewSet(viewsets.ModelViewSet):
    '''
    Instance 序列化
    '''

    queryset = models.Host.objects.filter(cate=1)
    serializer_class = serializers.HostListSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        # print(self.action)
        if self.action == 'list':
            return serializers.HostListSerializer
        return serializers.HostSerializer


# Node
class NodeModelViewSet(viewsets.ModelViewSet):
    '''
    Node 序列化
    '''
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeListSerializer
    pagination_class = LimitOffsetPagination


class HostRecordFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='name', method='filter_name')

    def filter_name(self, queryset, name, value):
        # print(queryset.filter(host_obj__name=value))
        return queryset.filter(host_obj__name=value)

    class Meta:
        model = models.HostRecord
        fields = ('id',)


# HostRecord
class HostRecordViewSet(viewsets.ModelViewSet):
    '''
    HostRecord 序列化
    '''
    queryset = models.HostRecord.objects.all()
    serializer_class = serializers.HostRecordListSerializer
    pagination_class = LimitOffsetPagination
    # filterset_class = HostRecordFilter
    filterset_fields = ['host_obj']


class IdracViewSet(viewsets.ModelViewSet):
    """
    iDRAC 序列化
    """
    queryset = models.IDRAC.objects.all()
    serializer_class = serializers.IDRACListSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.IDRACListSerializer
        return serializers.IDRACSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.task:
            obj.task.delete()

        if obj.host:
            obj.host.delete()
        res = super().destroy(request, *args, **kwargs)
        return res


class CmdRecordViewSet(viewsets.ModelViewSet):
    '''
    CmdRecord 序列化
    '''
    queryset = models.CmdRecord.objects.all()
    serializer_class = serializers.CmdRecordListSerializer
    pagination_class = LimitOffsetPagination


class RunUserViewSet(viewsets.ModelViewSet):
    '''
    RunUser 序列化
    '''
    queryset = models.RunUser.objects.all()
    serializer_class = serializers.RunUserListSerializer
    pagination_class = LimitOffsetPagination


# Process
class ProcessViewSet(viewsets.ModelViewSet):
    '''
    Process 序列化
    '''
    queryset = models.Process.objects.all()
    serializer_class = serializers.ProcessListSerializer
    pagination_class = LimitOffsetPagination


# HostProc
class HostProcViewSet(viewsets.ModelViewSet):
    '''
    HostProc 序列化
    '''
    queryset = models.HostProc.objects.all()
    serializer_class = serializers.HostProcListSerializer
    pagination_class = LimitOffsetPagination
