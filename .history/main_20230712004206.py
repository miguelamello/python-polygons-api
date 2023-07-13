from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from models import Provider, ServiceArea
from resources import ProviderResource, ServiceAreaResource, PolygonLookupResource

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/polygon'
mongo = PyMongo(app)
api = Api(app)
api.add_resource(ProviderResource, '/provider', '/providers/<string:provider_id>')
api.add_resource(ServiceAreaResource, '/service-areas', '/service-areas/<string:service_area_id>')
api.add_resource(PolygonLookupResource, '/polygons')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

