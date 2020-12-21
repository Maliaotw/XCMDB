from rest_framework import serializers
from hosts import models

from .host import HostSerializer


class IDRACSerializer(serializers.ModelSerializer):
    '''
    iDRAC
    '''
    host = HostSerializer(read_only=True)

    class Meta:
        model = models.IDRAC
        fields = "__all__"


class IDRACListSerializer(serializers.ModelSerializer):
    '''
    iDRAC List
    '''

    info = serializers.SerializerMethodField()

    def get_info(self, obj):
        # print(obj)
        if obj.host:
            return obj.host.get_info()
            # return "{}Cores {}GB {}G".format(obj.host.total_cores, obj.host.total_disk, obj.host.total_memory)

    class Meta:
        model = models.IDRAC
        # fields = "__all__"
        fields = ['id', 'idrac_ip', 'host', 'info']
