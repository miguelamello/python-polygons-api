from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from resources import ProviderResource, ServiceAreaResource, PolygonLookupResource
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Database configuration
load_dotenv('.env')
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('DB_NAME'),
    'host': os.getenv('DB_HOST')
    'port': os.getenv('DB_PORT')
    'username': os.getenv('DB_USERNAME')
    'password': os.getenv('DB_PASSWORD')
}

# Initialize database and API routes
db = MongoEngine(app) 
api = Api(app)
api.add_resource(ProviderResource, '/provider', '/provider/<string:provider_id>')
api.add_resource(ServiceAreaResource, '/service-area', '/service-area/<string:service_area_id>')
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

