from rest_framework import permissions
from rest_framework import serializers
from .models import Constellation

class ConstellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constellation
        fields = ['name', 'ra', 'dec']

class CoordinateSerializer(serializers.Serializer):
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)
