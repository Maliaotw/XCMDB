from rest_framework import serializers

from hosts import models

class HostProcListSerializer(serializers.ModelSerializer):
    '''
    idrac List
    '''

    class Meta:
        model = models.HostProc
        fields = "__all__"
