from rest_framework import serializers

from hosts import models



class HostRecordListSerializer(serializers.ModelSerializer):
    '''
    HostRecord List
    '''

    class Meta:
        model = models.HostRecord
        fields = "__all__"






