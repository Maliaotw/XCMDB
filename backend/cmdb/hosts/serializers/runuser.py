from rest_framework import serializers

from hosts import models



class RunUserListSerializer(serializers.ModelSerializer):
    '''
    idrac List
    '''

    class Meta:
        model = models.RunUser
        fields = "__all__"






