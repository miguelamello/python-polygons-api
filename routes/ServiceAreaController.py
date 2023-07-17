from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models.Provider import Provider
from models.ServiceArea import ServiceArea
from services.Utils import Utils
from decorators.api_key_required import api_key_required
from services.Redis import Redis
from routes.PolygonLookupController import PolygonLookupController
import json
from appconfig import env

# Redis Service
redis = Redis()

# Service Area Controller
class ServiceAreaController(Resource):
    @api_key_required
    def get(self, service_area_id):
        # Check if the data is already cached
        # If so, return the cached data
        # Otherwise, retrieve the data from the database
        # If error occurs, bypass the cache
        try:
            cached_data = redis.get_data(service_area_id)
            if cached_data:
                return json.loads(cached_data)
        except:
            pass
        
        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
            # Cache the result for future requests
            # Set expiration time to 1 hour
            # If error occurs, bypass the cache
            try:
                redis.set_data(service_area_id, service_area.to_json(), env['redis_ttl'])
            except:
                pass
            return json.loads(service_area.to_json())
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

    @api_key_required
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
        polygon_lookup = PolygonLookupController()
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

    @api_key_required
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
        polygon_lookup = PolygonLookupController()
        result = polygon_lookup.findPolygonProvider(data['vertices']['coordinates'], data['provider'])
        if len(result):
            if str(result[0].id) != str(service_area_id):
                if str(result[0].provider.id) == str(data['provider']):
                    return {'error': 'Polygon already exists for the provider'}, 400
        
        try:
            ServiceArea.objects(id=service_area_id).update_one(**data)
            # Cache the result for future requests
            # Set expiration time to 1 hour
            # If error occurs, bypass the cache
            try:
                data['provider'] = str(data['provider'])
                redis.set_data(service_area_id, json.dumps(data), env['redis_ttl'])
            except:
                pass
            return {'message': 'Service Area ' + service_area_id + ' updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    @api_key_required
    def delete(self, service_area_id):
        try:
            service_area = ServiceArea.objects.get(id=service_area_id)
            # Delete the key from cache
            try:
                redis.delete_data(service_area_id)
            except:
                pass
        except DoesNotExist:
            return {'error': 'Service Area ' + service_area_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            ServiceArea.objects(id=service_area_id).delete()
            return {'message': 'Service Area ' + service_area_id + ' deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404


