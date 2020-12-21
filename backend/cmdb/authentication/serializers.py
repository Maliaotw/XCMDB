from rest_framework import serializers
from . import models



class LoginSerializer(serializers.ModelSerializer):
    '''
    LoginSerializer
    '''

    type = serializers.CharField(source='get_type_display', required=False)
    reason = serializers.CharField(source='get_reason_display', required=False)
    status = serializers.CharField(source='get_status_display', required=False)
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)


    class Meta:
        model = models.UserLoginLog
        fields = '__all__'

