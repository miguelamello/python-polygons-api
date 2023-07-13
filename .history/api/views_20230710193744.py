from django.shortcuts import render

from rest_framework import viewsets
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

