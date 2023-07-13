from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from models import Provider, ServiceArea
from re

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/polygon'
mongo = PyMongo(app)
api = Api(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

