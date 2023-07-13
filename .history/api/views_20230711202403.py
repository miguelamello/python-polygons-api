from rest_framework_mongoengine import generics
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

class ProviderListCreateView(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProviderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ServiceAreaListCreateView(generics.ListCreateAPIView):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

class ServiceAreaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

class FindPolygonsByLatLngView(generics.ListAPIView):
    serializer_class = ServiceAreaSerializer

    def get_queryset(self):
        lat = float(self.request.query_params.get('lat'))
        lng = float(self.request.query_params.get('lng'))
        point = {"type": "Point", "coordinates": [lng, lat]}
        return ServiceArea.objects.filter(geojson__contains=point)
