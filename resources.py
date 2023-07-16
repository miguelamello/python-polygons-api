from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models import Provider, ServiceArea
from utils import Utils
import json, re, math
from decimal import Decimal, ROUND_HALF_EVEN

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
        data, err = Utils.formatServiceAreaPayload(data)
        
        if err != None:
            return {'error': err}, 400
     
        # Verify if the polygon already exists for the provider
        # Exit if already exists
        polygon_lookup = PolygonLookupResource()
        result = polygon_lookup.findPolygonProvider(data['vertices']['coordinates'], data['provider'])
        if len(result):
            if result[0].provider.id == data['provider']:
                return {'error': 'Polygon already exists for that provider'}, 400
        
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
        data, err = Utils.formatServiceAreaPayload(data)
        
        if err != None:
            return {'error': err}, 400
        
        # Before updating, verify if service area ID already exists
        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404
            
        # Before updating, verify if provider ID already exists
        # Exit if does not exists
        try:
            Provider.objects.get(id=data['provider'])
        except DoesNotExist:
            return {'error': 'Provider ' + str(data['provider']) + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404
        
        # Verify if the polygon already exists for the provider
        # Exit if already exists
        polygon_lookup = PolygonLookupResource()
        result = polygon_lookup.findPolygonProvider(data['vertices']['coordinates'], data['provider'])
        if len(result):
            if result[0].provider.id != service_area_id:
                if result[0].provider.id == data['provider']:
                    return {'error': 'Polygon already exists for the provider'}, 400
        
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

class ProviderServicesAreasResource(Resource):
    # Get all service areas from a provider
    def get(self, provider_id):
        try:
            service_areas = ServiceArea.objects(provider=provider_id)
            return json.loads(service_areas.to_json())
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404
    
    # Delete all service areas from a provider    
    def delete(self, provider_id):
        try:
            Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            result = ServiceArea.objects(provider=provider_id).delete()
            if result > 0:
                return {'message': 'Service Areas from provider ' + provider_id + ' deleted successfully'}
            else:
                return {'message': 'Provider ' + provider_id + ' does not have service areas'},
        except Exception as e:
            return {'error': str(e)}, 404

class PolygonLookupResource(Resource):
    # Search for the polygon that matches the coordinates
    def findPolygonProvider(self, coordinates, provider_id):
        return ServiceArea.objects(vertices__geo_within=coordinates, provider=provider_id)
    
    # Get all polygons that matches the coordinates
    def get(self):
        # Intercept payload
        raw_args = request.args
        
        # Format coordinates to expected syntax
        try: 
            lng = raw_args['lng'][:raw_args['lng'].index('.') + 5]
            lng = float(lng)
        except:
            return {'error': 'Longitude must be a valid geo coordinate: Ex: -73.9889'}, 404
        try:
            lat = raw_args['lat'][:raw_args['lat'].index('.') + 5]
            lat = float(lat)
        except Exception as e:
            return {'error': 'Latitude must be a valid geo coordinate: Ex: 40.7306'}, 404

        # Search for polygons that matches the coordinates
        raw_query = { 
            'vertices': { 
                '$geoIntersects': { 
                    '$geometry': { 
                        'type': 'Point', 
                        'coordinates': [ lng, lat ] 
                    } 
                } 
            } 
        }
        
        polygons = ServiceArea.objects(__raw__=raw_query).order_by('name')
        
        result = []
        for polygon in polygons:
            # Retrieve the associated provider information
            provider = Provider.objects.get(id=polygon.provider.id)
            
            # Append the result
            result.append({
                'name': polygon.name,
                'provider': provider.name,
                'price': polygon.price
            })

        return result

