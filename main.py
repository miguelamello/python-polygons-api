from flask import Flask, request, jsonify, render_template
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
api.add_resource(ProviderController, '/polygons/provider', '/polygons/provider/<string:provider_id>')
api.add_resource(ProviderServicesAreasController, '/polygons/provider/service-areas/<string:provider_id>')
api.add_resource(ServiceAreaController, '/polygons/service-area', '/polygons/service-area/<string:service_area_id>')
api.add_resource(PolygonLookupController, '/polygons/lookup')

# Handler for unhandled exceptions
'''@app.errorhandler(Exception)
def handle_exception(e):
    # Return the JSON response with the 500 status code
    return jsonify(error=str(e)), 500'''

@app.route("/")
def index():
    return ''

# Route for API documentation
@app.route("/polygons")
def app_doc():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8000)