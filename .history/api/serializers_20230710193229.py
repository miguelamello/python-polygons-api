from rest_framework import serializers
from .models import Provider, ServiceArea

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'email', 'phone_number', 'language', 'currency']

class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ['id', 'name', 'price', 'geojson']
