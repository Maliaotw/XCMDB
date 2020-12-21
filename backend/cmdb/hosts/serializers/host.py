from rest_framework import serializers

from hosts import models


class CPUListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CPU
        fields = "__all__"


class NICListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NIC
        fields = "__all__"


class DiskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disk
        fields = "__all__"


class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Memory
        fields = "__all__"


class NetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Net
        fields = "__all__"


class ProcListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.Process
        fields = "__all__"


class HostRecordListSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.HostRecord
        fields = ["title","summary","create_date"]


class HostSerializer(serializers.ModelSerializer):
    '''
    Host List
    '''
    cate = serializers.CharField(source='get_cate_display')
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    cpu = CPUListSerializer(many=True, read_only=True)
    nic = NICListSerializer(many=True, read_only=True)
    disk = DiskListSerializer(many=True, read_only=True)
    memory = MemoryListSerializer(many=True, read_only=True)
    hostnet = serializers.SerializerMethodField()
    hostproc = serializers.SerializerMethodField()
    hostrecord = HostRecordListSerializer(many=True, read_only=True)


    # def get_hostrecord(self,obj):
    #     print(obj)
        # return HostRecordListSerializer(obj.hostrecord_set.all(),many=True, read_only=True)

    def get_hostnet(self, obj):
        if obj.HostNet.all():
            hostnetobj = obj.HostNet.last()
            return NetListSerializer(hostnetobj.net.all(), many=True, read_only=True).data

    def get_hostproc(self,obj):
        if obj.HostProc.all():
            hostprocobj = obj.HostProc.last()
            return ProcListSerializer(hostprocobj.proc.all(), many=True, read_only=True).data

    class Meta:
        model = models.Host
        fields = "__all__"


class HostListSerializer(serializers.ModelSerializer):
    '''
    Host List
    '''
    cate = serializers.CharField(source='get_cate_display')
    enabled = serializers.CharField(source='get_enabled_display')
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.Host
        fields = "__all__"
