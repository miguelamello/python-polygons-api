from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models import Provider, ServiceArea
import json

class ProviderResource(Resource):
    def get(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
            return json.loads(provider.to_json())
        except Exception as e:
            return {'error': str(e)}, 404

    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        
        if Provider.objects(name=name):
            return {'error': 'Provider with the same name already exists'}, 400

        if Provider.objects(email=email):
            return {'error': 'Provider with the same email already exists'}, 400

        if Provider.objects(phone=phone):
            return {'error': 'Provider with the same phone already exists'}, 400
        
        try:
            provider = Provider(**data)
            provider.save()
            return {'message': 'Provider created successfully', 'id': str(provider.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def put(self, provider_id):
        data = request.get_json()
        try:
            Provider.objects(id=provider_id).update_one(**data)
            return {'message': 'Provider updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def delete(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            Provider.objects(id=provider_id).delete()
            return {'message': str(provider_id)}
            #return {'message': 'Provider deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404


class ServiceAreaResource(Resource):
    def get(self, service_area_id):
        service_area = ServiceArea.objects.get(id=service_area_id)
        return service_area.to_json()

    def post(self):
        data = request.get_json()
        try:
            service_area = ServiceArea(**data)
            service_area.save()
            return {'message': 'ServiceArea created successfully', 'id': str(service_area.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def put(self, service_area_id):
        data = request.get_json()
        try:
            ServiceArea.objects(id=service_area_id).update_one(**data)
            return {'message': 'ServiceArea updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def delete(self, service_area_id):
        ServiceArea.objects(id=service_area_id).delete()
        return {'message': 'ServiceArea deleted successfully'}


class PolygonLookupResource(Resource):
    def get(self):
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))

        polygons = ServiceArea.objects(
            geojson__geo_within_sphere=[[lng, lat], 0])
        result = []
        for polygon in polygons:
            result.append({
                'name': polygon.name,
                'provider': polygon.provider.name,
                'price': polygon.price
            })
        return result
