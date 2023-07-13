from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo = PyMongo(app)
api = Api(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

