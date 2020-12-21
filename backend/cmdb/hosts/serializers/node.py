from rest_framework import serializers

from hosts import models


class NodeListSerializer(serializers.ModelSerializer):
    '''
    IDC List
    '''

    class Meta:
        model = models.Node
        fields = "__all__"


