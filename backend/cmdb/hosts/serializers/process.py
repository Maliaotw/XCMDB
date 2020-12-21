from rest_framework import serializers

from hosts import models


class ProcessListSerializer(serializers.ModelSerializer):
    '''
    idrac List
    '''

    class Meta:
        model = models.Process
        fields = "__all__"

