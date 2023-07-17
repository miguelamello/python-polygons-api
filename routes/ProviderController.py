from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from models.Provider import Provider
from models.ServiceArea import ServiceArea
from services.Utils import Utils
from decorators.api_key_required import api_key_required
from services.Redis import Redis
import json
from appconfig import env

# Redis Service
redis = Redis()

# Provider Controller
class ProviderController(Resource):
    @api_key_required
    def get(self, provider_id):
        # Check if the data is already cached
        # If so, return the cached data
        # Otherwise, retrieve the data from the database
        # If error occurs, bypass the cache
        try:
            cached_data = redis.get_data(provider_id)
            if cached_data:
                return json.loads(cached_data)
        except:
            pass
        
        try:
            # Retrieve the provider from the database
            provider = Provider.objects.get(id=provider_id)
            # Cache the result for future requests
            # Set expiration time to 1 hour
            # If error occurs, bypass the cache
            try:
                redis.set_data(provider_id, provider.to_json(), env['redis_ttl'])
            except:
                pass
            return json.loads(provider.to_json())
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

    @api_key_required
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

    @api_key_required
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
            # Cache the result for future requests
            # Set expiration time to 1 hour
            # If error occurs, bypass the cache
            try:
                redis.set_data(provider_id, json.dumps(data), env['redis_ttl'])
            except:
                pass
            return {'message': 'Provider ' + provider_id + ' updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 404

    @api_key_required
    def delete(self, provider_id):
        try:
            provider = Provider.objects.get(id=provider_id)
        except DoesNotExist:
            return {'error': 'Provider ' + provider_id + ' does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 404

        try:
            Provider.objects(id=provider_id).delete()
            ServiceArea.objects(provider=provider_id).delete()
            # Delete the key from cache
            try:
                redis.delete_data(provider_id)
            except:
                pass
            return {'message': 'Provider ' + provider_id + ' deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404
