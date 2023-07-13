from rest_framework import serializers
from .models import Provider, ServiceArea

class ProviderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    language = serializers.CharField(max_length=50)
    currency = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return Provider.create(validated_data)

    def update(self, instance, validated_data):
        return Provider.update(instance['_id'], validated_data)

class ServiceAreaSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    geojson = serializers.JSONField()

    def create(self, validated_data):
        return ServiceArea.create(validated_data)

    def update(self, instance, validated_data):
        return ServiceArea.update(instance['_id'], validated_data)
