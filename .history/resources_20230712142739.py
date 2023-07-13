from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models import Provider, ServiceArea
from utils import Utils
import json, re

class ProviderResource(Resource):
    def get(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
            return json.loads(provider.to_json())
        except DoesNotExist:
            return {'error': 'Provider id does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

    def post(self):
        # Intercept payload
        data = request.get_json()
        name = ""
        email = ""
        phone = ""

        # Verify required fields
        # Exit if any of the required fields are missing
        if data.get('name') == None:
            return {'error': 'Name1 is required'}, 400

        if data.get('email') == None:
            return {'error': 'Email is required'}, 400

        if data.get('phone') == None:
            return {'error': 'Phone is required'}, 400

        if len(data.get('name').stri) == 0:
            return {'error': 'Name1 can not be empty'}, 400

        # Format data to expected syntaxe
        if data.get('name'):
            data['name'] = data.get('name').strip().title()
            name = data.get('name')

        if data.get('email'):
            data['email'] = data.get('email').strip().lower()
            email = data.get('email')
        
        if data.get('phone'):
            data['phone'] = Utils.toNumber(data.get('phone').strip())
            phone = data.get('phone')
        
        if data.get('language'):
            data['language'] = data.get('language').strip().title()
        
        if data.get('currency'):
            data['currency'] = data.get('currency').strip().upper()
        
        # Verify if provider entries already exists
        # Exit if any of the entries already exists
        if Provider.objects(name=name):
            return {'error': 'Provider with the same name already exists'}, 400

        if Provider.objects(email=email):
            return {'error': 'Provider with the same email already exists'}, 400

        if Provider.objects(phone=phone):
            return {'error': 'Provider with the same phone already exists'}, 400

        if Utils.isEmail(email) == False:
            return {'error': 'Invalid email format'}, 400
        
        # Create provider
        try:
            provider = Provider(**data)
            provider.save()
            return {'message': 'Provider created successfully', 'id': str(provider.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    def put(self, provider_id):
        data = request.get_json()
        try:
            Provider.objects(id=provider_id).update_one(**data)
            return {'message': 'Provider updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    def delete(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            Provider.objects(id=provider_id).delete()
            return {'message': 'Provider deleted successfully'}
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