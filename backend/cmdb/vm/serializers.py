from rest_framework import serializers

from . import models
import inspect
import logging

import ipaddress

class NetWorkStaticListSerializer(serializers.ModelSerializer):
    '''
    NetWork
    '''

    class Meta:
        model = models.NetWorkStatic
        fields = "__all__"

class NetWorkStaticSerializer(serializers.ModelSerializer):
    '''
    NetWork
    '''

    class Meta:
        model = models.NetWorkStatic
        fields = "__all__"

class NetWorkStaticUpdateSerializer(serializers.ModelSerializer):
    '''
    NetWork
    '''

    class Meta:
        model = models.NetWorkStatic
        # fields = "__all__"
        exclude = ['id']


class NetWorkListSerializer(serializers.ModelSerializer):
    '''
    NetWork
    '''

    class Meta:
        model = models.NetWork
        fields = "__all__"


class DatastoreListSerializer(serializers.ModelSerializer):
    '''
    Datastore
    '''

    capacity = serializers.SerializerMethodField()
    freeSpace = serializers.SerializerMethodField()
    provisioned = serializers.SerializerMethodField()

    def size(self, _capacity):
        capacity = _capacity
        for unit in ['KB', 'MB', 'GB', 'TB']:
            capacity = capacity / 1024
            if capacity < 1000:
                return "%s %s" % (round(capacity, 2), unit)

    def get_capacity(self, obj):
        return self.size(obj.capacity)

    def get_freeSpace(self, obj):
        return self.size(obj.freeSpace)

    def get_provisioned(self, obj):
        return self.size(obj.provisioned)

    class Meta:
        model = models.DataStore
        fields = "__all__"


class InstanceSerializer(serializers.ModelSerializer):
    '''
    Instance
    '''

    class Meta:
        model = models.Instance
        fields = "__all__"
        # exclude = ['power_state']


class InstanceListSerializer(serializers.ModelSerializer):
    '''
    Instance
    '''

    hw_power_status = serializers.CharField(source='get_hw_power_status_display')
    info = serializers.SerializerMethodField()
    host = serializers.CharField(source='host.name', read_only=True)
    network = NetWorkListSerializer()
    datastore = DatastoreListSerializer()

    def get_info(self, obj):
        return "{}CPU {}G {}G".format(obj.hw_processor_count, obj.hw_memtotal_mb / 1024, obj.capacity)

    class Meta:
        model = models.Instance
        fields = "__all__"


class NetWorkSerializer(serializers.ModelSerializer):
    '''
    NetWork
    '''

    def validate_iprange(self, value):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))

        # iprange = self.initial_data['iprange']
        self.iprange_obj = ipaddress.ip_network(value, strict=False)
        if self.iprange_obj.num_addresses != 1:
            return value
        else:
            raise serializers.ValidationError("IP範圍錯誤")

    def validate_gateway(self, value):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))

        # gateway = self.initial_data['gateway']
        if ipaddress.IPv4Address(value) in self.iprange_obj:
            return value
        else:
            raise serializers.ValidationError("gateway錯誤")

    def validate(self, data):
        """
        Check that start is before finish.
        """
        data.update({
            "total": len(list(self.iprange_obj.hosts())) - 1
        })
        return data

    class Meta:
        model = models.NetWork
        fields = "__all__"


class HostCreatrListSerializer(serializers.ModelSerializer):
    '''
    Host
    '''

    datastore = serializers.SerializerMethodField()
    # template = serializers.SerializerMethodField()

    def get_datastore(self, obj):
        # print(obj)
        return DatastoreListSerializer(obj.datastore.filter(status=True), many=True).data
    #
    # def get_template(self, obj):
    #     # print(obj)
    #     return InstanceSerializer(obj.guests.filter(hw_is_template=True), many=True).data

    class Meta:
        model = models.Host
        fields = "__all__"


class HostListSerializer(serializers.ModelSerializer):
    '''
    Host
    '''

    last_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    network = NetWorkListSerializer(many=True, read_only=True)
    datastore = DatastoreListSerializer(many=True, read_only=True)
    template = serializers.SerializerMethodField()
    cluster = serializers.CharField(source='cluster.name')

    used_vcpus = serializers.SerializerMethodField()
    guests_count = serializers.SerializerMethodField()
    ansible_memfree_gb = serializers.SerializerMethodField()
    ansible_memtotal_gb = serializers.SerializerMethodField()

    def get_template(self, obj):
        # print(obj)
        return InstanceSerializer(obj.guests.filter(hw_is_template=True), many=True).data

    def get_ansible_memfree_gb(self, obj):
        return round((obj.ansible_memtotal_mb - obj.ansible_memfree_mb) / 1024, 2)

    def get_ansible_memtotal_gb(self, obj):
        return round(obj.ansible_memtotal_mb / 1024, 2)

    def get_used_vcpus(self, obj):
        # print(obj)
        return sum([i.hw_processor_count for i in obj.guests.all()])

    def get_guests_count(self, obj):
        return obj.guests.all().count()

    class Meta:
        model = models.Host
        fields = "__all__"


class HostSerializer(serializers.ModelSerializer):
    '''
    Host
    '''

    # network = NetWorkListSerializer(many=True, read_only=True)
    # datastore = DatastoreListSerializer(many=True, read_only=True)
    last_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.Host
        fields = "__all__"


class VMListSerializer(serializers.ModelSerializer):
    '''
    VM
    '''

    status = serializers.CharField(source='get_status_display')
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.VM
        fields = "__all__"


class InsSerializer(serializers.Serializer):
    '''
    VM Instance
    '''

    hostname = serializers.CharField()
    type = serializers.SerializerMethodField()
    vcpu = serializers.IntegerField()
    memory = serializers.IntegerField()
    disk_size = serializers.IntegerField()

    def get_type(self, obj):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        type = self.initial_data.get('type')
        if type in ['ECS', 'RDS']:
            return type
        else:
            raise serializers.ValidationError("類型錯誤")


class ClusterListSerializer(serializers.ModelSerializer):
    '''
       VM cluster List
    '''

    esxi_num = serializers.SerializerMethodField()
    vm_num = serializers.SerializerMethodField()

    network = serializers.SerializerMethodField()
    host = serializers.SerializerMethodField()
    # template = serializers.SerializerMethodField()


    def get_esxi_num(self, obj):
        # print(obj.host.all().count())
        return obj.host.all().count()

    def get_vm_num(self, obj):
        # print(obj.instance.all().count())
        return obj.instance.all().count()

    # def get_template(self, obj):
    #     # obj.instance.filter(hw_is_template=True).all()
    #     return InstanceListSerializer(obj.instance.filter(hw_is_template=True).all(), many=True).data

    def get_network(self, obj):
        # print(obj)
        return NetWorkListSerializer(obj.network.filter(status=True).all(), many=True).data

    def get_host(self, obj):
        # print(obj.host.all().count())
        return HostCreatrListSerializer(obj.host.all(), many=True).data

    class Meta:
        model = models.Cluster
        fields = "__all__"


class ClusterRetrieveSerializer(serializers.ModelSerializer):
    '''
    VM cluster Retrieve
    '''

    esxi_num = serializers.SerializerMethodField()
    vm_num = serializers.SerializerMethodField()
    network = NetWorkListSerializer(many=True)

    def get_esxi_num(self, obj):
        # print(obj.host.all().count())
        return obj.host.all().count()

    def get_vm_num(self, obj):
        # print(obj.instance.all().count())
        return obj.instance.all().count()

    class Meta:
        model = models.Cluster
        fields = "__all__"


class ClusterSerializer(serializers.ModelSerializer):
    '''
    VM cluster
    '''


    class Meta:
        model = models.Cluster
        fields =  ['remark']


class DataStoreUpdateSerializer(serializers.ModelSerializer):
    '''
    VM cluster
    '''

    class Meta:
        model = models.DataStore
        fields = ['remark', 'status']


class NetWorkUpdateSerializer(serializers.ModelSerializer):
    '''
    VM cluster
    '''

    class Meta:
        model = models.NetWork
        fields = ['remark', 'status','dhcp']
