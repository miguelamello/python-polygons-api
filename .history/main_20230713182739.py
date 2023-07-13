from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from resources import ProviderResource, ServiceAreaResource, PolygonLookupResource
from appconfig import env

app = Flask(__name__)

# Database configuration
print(env['mongo_host'])

app.config['MONGODB_SETTINGS'] = {'host': env['mongo_host']}
 
# Initialize database and API routes
db = MongoEngine()
db.init_app(app)
api = Api(app)
api.add_resource(ProviderResource, '/provider','/provider/<string:provider_id>')
api.add_resource(ServiceAreaResource, '/service-area','/service-area/<string:service_area_id>')
api.add_resource(PolygonLookupResource, '/polygons')

# Handler for unhandled exceptions


@app.errorhandler(Exception)
def handle_exception(e):
    # Return the JSON response with the 500 status code
    return jsonify(error=str(e)), 500

# Route for API documentation


@app.route("/")
def hello_world():
    return "Polygon API"
