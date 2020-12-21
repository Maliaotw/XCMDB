from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from common import serializers
# Create your views here.
class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        s = serializers.UserProfileSerializer(self.request.user)
        return Response(s.data)