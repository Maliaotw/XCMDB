from rest_framework import serializers

from assets import models
from django.contrib.contenttypes.models import ContentType


# Tag

class TagSerializer(serializers.ModelSerializer):
    '''
    TAG
    '''

    class Meta:
        model = models.Tag
        fields = "__all__"


# ContentType
class ContentTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = ContentType
        fields = "__all__"


# IDC
class IDCSerializer(serializers.ModelSerializer):
    '''
    IDC
    '''

    rackunit = serializers.SerializerMethodField()

    def get_rackunit(self,obj):
        # print(obj)
        return obj.rack.count()


    class Meta:
        model = models.IDC
        fields = "__all__"


# ISP
class ISPSerializer(serializers.ModelSerializer):
    '''
    ISP
    '''

    class Meta:
        model = models.ISP
        fields = "__all__"


# Assets
class AssetsSerializer(serializers.ModelSerializer):
    '''
    Asset
    '''

    idc = serializers.IntegerField(source='rack.idc.id', read_only=True)
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    device_type_id = serializers.CharField(source='get_device_type_id_display', required=False)

    class Meta:
        model = models.Asset
        # fields = "__all__"
        exclude = ['content_type']


class AssetsListSerializer(serializers.ModelSerializer):
    '''
    Asset List
    '''
    device_type_id = serializers.CharField(source='get_device_type_id_display', required=False)
    device_status_id = serializers.CharField(source='get_device_status_id_display', required=False)
    rack = serializers.CharField(source='rack.name', required=False)
    tag = serializers.CharField(source='tag.name', required=False)
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.Asset
        fields = "__all__"


# RackUnit
class RackUnitSerializer(serializers.ModelSerializer):
    '''
    RackUnit 機櫃使用表
    '''

    class Meta:
        model = models.RackUnit
        fields = ["position", "num"]


# RackUnit
class RackUnitListSerializer(serializers.ModelSerializer):
    '''
    RackUnit 機櫃使用表
    '''
    name = serializers.CharField(source='name.name')
    asset = AssetsListSerializer()

    # position = serializers.CharField(source='get_position_display')

    class Meta:
        model = models.RackUnit
        fields = "__all__"


# Rack

class RackDetailSerializer(serializers.ModelSerializer):
    '''
    Rack 機櫃
    '''
    rackunit = RackUnitListSerializer(many=True, read_only=True)
    isp = ISPSerializer(many=True, read_only=True)
    posrange = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def _range(self, obj):
        ran = range(1, obj.height + 1)
        ran = list(ran)
        ran.reverse()
        return ran

    def get_posrange(self, obj):
        # print(obj)
        ran = self._range(obj)
        ret = []
        inrack_list = self._inrack(obj)

        for i in ran:
            data = {}
            data['num'] = i
            data['position'] = ''
            data['name'] = ''
            data['manage_ip'] = ''
            data['size'] = ''

            rackunit_obj = obj.rackunit.filter(num=i)
            if rackunit_obj:
                rackunit_obj = rackunit_obj.first()
                data['position'] = rackunit_obj.get_position_display()
                data['name'] = rackunit_obj.asset.name
                data['manage_ip'] = rackunit_obj.asset.content_object.manage_ip
                data['size'] = rackunit_obj.asset.size
                data['disabled'] = False

            elif i in inrack_list:
                data['disabled'] = True
            else:
                data['disabled'] = False
            ret.append(data)

        return ret

    def _inrack(self, obj):
        insize = []
        for i in obj.rackunit.all():
            if not i.num:
                continue

            if i.asset.size > 1:
                for num in range(i.num - i.asset.size + 1, i.num + 1):
                    insize.append(num)
            else:
                insize.append(i.num)

        return insize

    def get_size(self, obj):

        ret = []
        inrack_list = self._inrack(obj)

        for i in self._range(obj):

            data = {
                'value': i,
                'label': i
            }
            if i in inrack_list:
                # print('in %s' % i)
                data['disabled'] = True
            else:
                # print('notin %s' % i)
                data['disabled'] = False

            ret.append(data)

        # r3 = list(set(r1) - set(r2))
        # r3.reverse()
        return ret

    class Meta:
        model = models.Rack
        fields = "__all__"


class RackSerializer(serializers.ModelSerializer):
    '''
    Rack 機櫃
    '''
    rackunit = RackUnitListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Rack
        fields = "__all__"


class RackListSerializer(serializers.ModelSerializer):
    '''
    Rack 機櫃
    '''

    idc = serializers.SerializerMethodField()
    # asset = AssetsListSerializer(many=True, read_only=True)
    asset = serializers.SerializerMethodField()
    isp = ISPSerializer(many=True, read_only=True)
    used = serializers.SerializerMethodField()

    def get_used(self,obj):
        # print(obj)
        return int((sum([i.asset.size for i in  obj.rackunit.all()]) / obj.height )*100)

    def get_idc(self, obj):
        # print(obj)
        return "%s" % str(obj.idc)

    def get_asset(self, obj):
        # print(obj)
        return "%s" % len(obj.asset.all())

    class Meta:
        model = models.Rack
        fields = "__all__"


# IDC

class IDCListSerializer(serializers.ModelSerializer):
    '''
    IDC List
    '''
    # rack = serializers.StringRelatedField(many=True)
    # rack = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # rack = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='rack-detail'
    # )

    rack = RackSerializer(many=True, read_only=True)

    class Meta:
        model = models.IDC
        fields = "__all__"


# NetworkDevice
class NetworkDeviceSerializer(serializers.ModelSerializer):
    '''
    NetworkDevice
    '''

    # type = serializers.ChoiceField(models.NetworkDevice.type_choices)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.NetworkDevice
        # fields = "__all__"
        exclude = ['intranet_ip', ]


class NetworkDeviceListSerializer(serializers.ModelSerializer):
    '''
    NetworkDevice List
    '''

    sub_asset_type = serializers.CharField(source='get_sub_asset_type_display')
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.NetworkDevice
        fields = "__all__"


# Storage
class StorageNicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StorageNic
        fields = "__all__"


class StorageDiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StorageDisk
        fields = "__all__"


class StorageCtlSerializer(serializers.ModelSerializer):
    storagenic = StorageNicSerializer(many=True, read_only=True)

    class Meta:
        model = models.StorageCtl
        fields = "__all__"


class StorateListSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = models.Storage
        fields = "__all__"


class StorateSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    latest_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    storagectl = StorageCtlSerializer(many=True, read_only=True)
    storagedisk = StorageDiskSerializer(many=True, read_only=True)

    class Meta:
        model = models.Storage
        fields = "__all__"
