from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response
from rest_framework.generics import RetrieveAPIView
from assets import models
from assets import serializers
from hosts.serializers import HostSerializer
from django_filters import rest_framework as filters

class AssetTypeAPIView(APIView):
    '''
    資產 類型
        (1, '服務器'),
        (2, '網路設備'),
    '''

    def get(self, request, *args, **kwargs):
        return Response(models.Asset.device_type_choices)

class AssetStatusAPIView(APIView):
    '''
    資產 狀態
        (1, '上架'),
        (2, '線上'),
        (3, '離線'),
        (4, '下架'),
    '''

    def get(self, request, *args, **kwargs):
        return Response(models.Asset.device_status_choices)

class NetdeviceStatusAPIView(APIView):


    def get(self, request, *args, **kwargs):
        return Response(models.NetworkDevice.type_choices)

class AssetsFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = models.Asset
        fields = ('name', 'device_type_id', 'device_status_id', 'rack')

class AssetsModelViewSet(viewsets.ModelViewSet):
    '''
    資產 序列化
    '''

    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetsListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AssetsFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['rack'] = serializers.RackListSerializer(models.Rack.objects.all(), many=True).data

        return response
    
    
    def get_serializer_class(self):
        # print(self.__class__.__name__,'get_serializer_class',self.action)

        if self.action == 'list':
            return serializers.AssetsListSerializer
        return serializers.AssetsSerializer

    def retrieve(self, request, *args, **kwargs):
        # 資產詳細
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if instance.device_type_id == 1:
            content = HostSerializer(instance.content_object)
        elif instance.device_type_id == 2:
            content = serializers.NetworkDeviceSerializer(instance.content_object)
        else:
            content = serializers.StorateSerializer(instance.content_object)



        data = serializer.data
        data.update({'content_object': content.data})
        data.update({'idc_list': serializers.IDCSerializer(models.IDC.objects.all(),many=True).data})
        data.update({'rack_list':serializers.RackListSerializer(models.Rack.objects.all(),many=True).data})
        data.update({'tag_list': serializers.TagSerializer(models.Tag.objects.all(), many=True).data})
        return Response(data)



class TagFilter(filters.FilterSet):

    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = models.Tag
        fields = ('name',)

class TAGModelViewSet(viewsets.ModelViewSet):
    '''
    TAG序列化
    '''

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = TagFilter


class IDCModelViewSet(viewsets.ModelViewSet):
    '''
    IDC序列化
    '''

    queryset = models.IDC.objects.all()
    serializer_class = serializers.IDCSerializer
    pagination_class = LimitOffsetPagination


class RackFilter(filters.FilterSet):

    class Meta:
        model = models.Rack
        fields = ('idc',)



# Rack
class RackDetailAPIView(RetrieveAPIView):
    '''
    機櫃詳細
    '''
    queryset = models.Rack.objects.all()
    serializer_class = serializers.RackDetailSerializer

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        # print(self.__class__.__name__, "get")
        # print(ret.data)
        return ret


class RackModelViewSet(viewsets.ModelViewSet):
    '''
    機櫃序列化
    '''

    queryset = models.Rack.objects.all()
    serializer_class = serializers.RackSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RackFilter

    def get_serializer_class(self):
        # print(self.__class__.__name__, self.action)
        if self.action == 'list':
            return serializers.RackListSerializer
        return serializers.RackSerializer


class RackUnitModelViewSet(viewsets.ModelViewSet):
    '''
    機櫃使用表 序列化
    '''
    queryset = models.RackUnit.objects.all()
    serializer_class = serializers.RackUnitListSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        # print(self.__class__.__name__, self.action)

        if self.action == 'list':
            return serializers.RackUnitListSerializer
        return serializers.RackUnitSerializer


# ISP

class ISPModelViewsSet(viewsets.ModelViewSet):
    '''
    ISP 序列化
    '''

    queryset = models.ISP.objects.all()
    serializer_class = serializers.ISPSerializer
    pagination_class = LimitOffsetPagination




class NetDeviceFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    manage_ip = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = models.NetworkDevice
        fields = ('name', 'sub_asset_type', 'manage_ip', 'port_num')



class NetDeviceModelViewsSet(viewsets.ModelViewSet):
    '''
    網路設備 序列化
    '''

    queryset = models.NetworkDevice.objects.all()
    serializer_class = serializers.NetworkDeviceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NetDeviceFilter

    def retrieve(self, request, *args, **kwargs):
        # 網路設備 詳細
        # print(self.action) # retrieve

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data.update({'type': models.NetworkDevice.type_choices})
        return Response(data)


    def get_serializer_class(self):
        # print(self.action)

        if self.action == 'list':
            return serializers.NetworkDeviceListSerializer
        return serializers.NetworkDeviceSerializer

# Storage

class StorageModelViewsSet(viewsets.ModelViewSet):
    queryset = models.Storage.objects.all()
    serializer_class = serializers.StorateSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        # print(self.action)

        if self.action == 'list':
            return serializers.StorateListSerializer
        return serializers.StorateSerializer


