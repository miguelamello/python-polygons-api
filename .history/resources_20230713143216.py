from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models import Provider, ServiceArea
from utils import Utils
from bson import ObjectId
import json, re

class ProviderResource(Resource):
    def get(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
            return json.loads(provider.to_json())
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

    def post(self):
        # Intercept payload
        data = request.get_json()

        # Verify required fields
        # Exit if any of the them are missing or empty
        response = Utils.validateProviderFields(data)
        if response != True:
            return response

        # Format payload to expected syntaxe
        data = Utils.formatProviderPayload(data)
        
        # Verify if provider entries already exists
        # Exit if any of the entries already exists
        if Provider.objects(name=data['name']):
            return {'error': 'Provider with the same name already exists'}, 400

        if Provider.objects(email=data['email']):
            return {'error': 'Provider with the same email already exists'}, 400

        if Provider.objects(phone=data['phone']):
            return {'error': 'Provider with the same phone already exists'}, 400

        if Utils.isEmail(data['email']) == False:
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
        # Intercept payload
        data = request.get_json()

        # Verify required fields
        # Exit if any of the them are missing or empty
        response = Utils.validateProviderFields(data)
        if response != True:
            return response

        # Format payload to expected syntaxe
        data = Utils.formatProviderPayload(data)

        try:
            provider = Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            Provider.objects(id=provider_id).update_one(**data)
            return {'message': 'Provider ' + provider_id + ' updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    def delete(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            Provider.objects(id=provider_id).delete()
            return {'message': 'Provider ' + provider_id + ' deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404


class ServiceAreaResource(Resource):
    def get(self, service_area_id):
        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
            return json.loads(service_area.to_json())
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

    def post(self):
        # Intercept payload
        data = request.get_json()

        # Verify required fields
        # Exit if any of the them are missing or empty
        response = Utils.validateServiceAreaFields(data)
        if response != True:
            return response
        
        # Format payload to expected syntaxe
        data = Utils.formatServiceAreaPayload(data)

        # Insert missing Geoposition Type 
        if data.get('geopos', {}).get('type') == None:
            data['geopos']['type'] = "Point"
        
        # Verify if provider entries already exists
        # Exit if any of the entries already exists
        if ServiceArea.objects(name=data['geopos']['coordinates']):
            return {'error': 'Service Area with the same Geoposition already exists'}, 400
        
        # Create provider
        try:
            service_area = ServiceArea(**data)
            service_area.save()
            return {'message': 'Service Area created successfully', 'id': str(service_area.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    def put(self, service_area_id):
        # Intercept payload
        data = request.get_json()

        # Verify required fields
        # Exit if any of the them are missing or empty
        response = Utils.validateServiceAreaFields(data)
        if response != True:
            return response

        # Format payload to expected syntaxe
        data = Utils.formatServiceAreaPayload(data)

        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            ServiceArea.objects(id=service_area_id).update_one(**data)
            return {'message': 'Service Area ' + service_area_id + ' updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    def delete(self, service_area_id):
        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            ServiceArea.objects(id=service_area_id).delete()
            return {'message': 'Service Area ' + service_area_id + ' deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404


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