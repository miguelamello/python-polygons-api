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

# Polygon Lookup Controller
class PolygonLookupController(Resource):
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

