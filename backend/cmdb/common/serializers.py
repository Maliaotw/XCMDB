from rest_framework import serializers
from common import models


class UserProfileSerializer(serializers.ModelSerializer):
    '''
    序列化用戶表
    '''

    class Meta:
        model = models.UserProfile
        fields = ('username', 'email')

