from rest_framework import serializers

from hosts import models



class BusUnitListSerializer(serializers.ModelSerializer):
    '''
    idrac List
    '''

    class Meta:
        model = models.BusinessUnit
        fields = "__all__"






