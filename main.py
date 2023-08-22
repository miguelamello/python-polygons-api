from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from functools import wraps
from marshmallow import Schema, fields, ValidationError
from routes.ProviderController import ProviderController
from routes.ProviderServicesAreasController import ProviderServicesAreasController
from routes.ServiceAreaController import ServiceAreaController
from routes.PolygonLookupController import PolygonLookupController
from appconfig import env

app = Flask(__name__)

# Database configuration
app.config['MONGODB_SETTINGS'] = { 'host': env['mongo_host'] }
 
# Initialize database and API routes
db = MongoEngine()
db.init_app(app)
api = Api(app)
api.add_resource(ProviderController, '/provider', '/provider/<string:provider_id>')
api.add_resource(ProviderServicesAreasController, '/service-areas/<string:provider_id>')
api.add_resource(ServiceAreaController, '/service-area', '/service-area/<string:service_area_id>')
api.add_resource(PolygonLookupController, '/lookup')

# Redirect to API documentation
@app.route("/") 
def redirect_to():
    return redirect(url_for('app_doc'))

# Route for API documentation
@app.route("/reference")
def app_doc():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8000)