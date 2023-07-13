from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from resources import ProviderResource, ServiceAreaResource, PolygonLookupResource

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'polygon',
    'host': 'mongodb://localhost:27017/polygon'
}

db = MongoEngine(app) 
api = Api(app)
api.add_resource(ProviderResource, '/provider', '/provider/<string:provider_id>')
api.add_resource(ServiceAreaResource, '/service-area', '/service-area/<string:service_area_id>')
api.add_resource(PolygonLookupResource, '/polygons')

@app.errorhandler(Exception)
def handle_exception(e):
    # Create a dictionary with the error message
    error_data = {
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred.'
    }
    
    # Return the JSON response with the 500 status code
    return jsonify(error=str(e)), 500

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

