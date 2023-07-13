from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

class ProviderListCreateView(APIView):
    def get(self, request):
        providers = Provider.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            provider = serializer.save()
            return Response(ProviderSerializer(provider).data, status=201)
        return Response(serializer.errors, status=400)

class ProviderRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        provider = Provider.get(pk)
        if provider:
            serializer = ProviderSerializer(provider)
            return Response(serializer.data)
        return Response(status=404)

    def put(self, request, pk):
        provider = Provider.get(pk)
        if provider:
            serializer = ProviderSerializer(provider, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=404)

    def delete(self, request, pk):
        provider = Provider.get(pk)
        if provider:
            Provider.delete(pk)
            return Response(status=204)
        return Response(status=404)

class ServiceAreaListCreateView(APIView):
    def get(self, request):
        service_areas = ServiceArea.all()
        serializer = ServiceAreaSerializer(service_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceAreaSerializer(data=request.data)
        if serializer.is_valid():
            service_area = serializer.save()
            return Response(ServiceAreaSerializer(service_area).data, status=201)
        return Response(serializer.errors, status=400)

class ServiceAreaRetrieveUpdateDestroyView(APIView):
    def get(self, request,
