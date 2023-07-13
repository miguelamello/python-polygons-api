from rest_framework import serializers
from .models import Provider, ServiceArea

class ProviderSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class ServiceAreaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ServiceArea
        fields = '__all__'
