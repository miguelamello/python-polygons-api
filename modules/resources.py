from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import ValidationError, DoesNotExist
from modules.models import Provider, ServiceArea
from modules.utils import Utils
from decorators.apikeyrequired import api_key_required
import json, redis
from appconfig import env

# Redis connection
r = redis.Redis(host=env['redis_host'], port=6379, db=0)

# Provider Controller
class ProviderResource(Resource):
    @api_key_required
    def get(self, provider_id):
        # Check if the data is already cached
        # If so, return the cached data
        # Otherwise, retrieve the data from the database
        # If error occurs, bypass the cache
        try:
            cached_data = r.get(provider_id)
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
                r.setex(provider_id, env['redis_ttl'], provider.to_json())
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
                r.setex(provider_id, env['redis_ttl'], json.dumps(data))
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
                r.delete(provider_id)
            except:
                pass
            return {'message': 'Provider ' + provider_id + ' deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 404

# Service Area Controller
class ServiceAreaResource(Resource):
    @api_key_required
    def get(self, service_area_id):
        # Check if the data is already cached
        # If so, return the cached data
        # Otherwise, retrieve the data from the database
        # If error occurs, bypass the cache
        try:
            cached_data = r.get(service_area_id)
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
                r.setex(service_area_id, env['redis_ttl'], service_area.to_json())
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
        polygon_lookup = PolygonLookupResource()
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
                r.setex(service_area_id, env['redis_ttl'], json.dumps(data))
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
                r.delete(service_area_id)
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

# Provider Service Areas Controller
class ProviderServicesAreasResource(Resource):
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

# Polygon Lookup Controller
class PolygonLookupResource(Resource):
    # Search for the polygon that matches the coordinates
    def findPolygonProvider(self, coordinates, provider_id):
        return ServiceArea.objects(vertices__geo_within=coordinates, provider=provider_id)
    
    # Get all polygons that matches the coordinates
    @api_key_required
    def get(self):
        # Intercept payload
        raw_args = request.args
        
        # Format coordinates to expected syntax
        try: 
            lng = raw_args['longitude']
            lng = lng[:lng.index('.') + 5]
            lng = float(lng)
        except:
            return {'error': 'Longitude must be a valid geo coordinate: Ex: -73.9889'}, 404
        try:
            lat = raw_args['latitude']
            lat = lat[:lat.index('.') + 5]
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

