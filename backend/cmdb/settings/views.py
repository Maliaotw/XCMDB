from rest_framework import permissions, status
from rest_framework.views import APIView, Response

from . import serializers

# Create your views here.


class IdracSettingView(APIView):
    serializers_class = serializers.IdracSettingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        serializer = self.serializers_class()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VcenterSettingView(APIView):
    """ """

    serializers_class = serializers.VCENTERSettingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        serializer = self.serializers_class()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LDAPSettingView(APIView):
    serializers_class = serializers.LDAPSettingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        serializer = self.serializers_class()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
