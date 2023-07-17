from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models import *
from library import Utils
from decorators.api_key_required import api_key_required
import json, redis
from appconfig import env

# Redis connection
r = redis.Redis(host=env['redis_host'], port=6379, db=0)


# Provider Service Areas Controller
class ProviderServicesAreasController(Resource):
    # Get all service areas from a provider
    @api_key_required
    def get(self, provider_id):
        try:
            service_areas = ServiceArea.objects(provider=provider_id).limit(1000)
            # Convert the ServiceArea objects to JSON using to_json() method
            documents = []
            for service_area in service_areas:
                json_data = service_area.to_json()
                documents.append(json.loads(json_data))
            return documents
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404
    
    # Delete all service areas from a provider    
    @api_key_required
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



