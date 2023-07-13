from pymongo import MongoClient
from django.conf import settings

client = MongoClient(
    host=settings.DATABASES['mongodb']['OPTIONS']['host'],
    port=settings.DATABASES['mongodb']['OPTIONS']['port']
)
db = client[settings.DATABASES['mongodb']['NAME']]

class Provider:
    collection = db['providers']

    @classmethod
    def all(cls):
        return cls.collection.find()

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get(cls, provider_id):
        return cls.collection.find_one({'_id': provider_id})

    @classmethod
    def update(cls, provider_id, data):
        return cls.collection.update_one({'_id': provider_id}, {'$set': data})

    @classmethod
    def delete(cls, provider_id):
        return cls.collection.delete_one({'_id': provider_id})

class ServiceArea:
    collection = db['service_areas']

    @classmethod
    def all(cls):
        return cls.collection.find()

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get(cls, service_area_id):
        return cls.collection.find_one({'_id': service_area_id})

    @classmethod
    def update(cls, service_area_id, data):
        return cls.collection.update_one({'_id': service_area_id}, {'$set': data})

    @classmethod
    def delete(cls, service_area_id):
        return cls.collection.delete_one({'_id': service_area_id})
