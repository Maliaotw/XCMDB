from rest_framework import serializers

from hosts import models



class CmdRecordListSerializer(serializers.ModelSerializer):
    '''
    idrac List
    '''

    class Meta:
        model = models.CmdRecord
        fields = "__all__"


