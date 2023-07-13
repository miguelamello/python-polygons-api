#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @action(detail=False, methods=['get'])
    def get_polygons(self, request):
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))

        point = GEOSGeometry(f'POINT({lng} {lat})', srid=4326)
        polygons = ServiceArea.objects.filter(geojson__contains=point)

        response_data = []
        for polygon in polygons:
            if polygon.geojson['type'] == 'Polygon' and polygon.geojson['coordinates']:
                polygon_geom = GEOSGeometry(
                    json.dumps(polygon.geojson), srid=4326
                )
                if polygon_geom and polygon_geom.contains(point):
                    response_data.append({
                        'name': polygon.name,
                        'provider_name': polygon.provider.name,
                        'price': polygon.price
                    })

        return Response(response_data)


