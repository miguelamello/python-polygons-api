from mongoengine import Document, StringField, EmailField, FloatField, PolygonField, ReferenceField
import json

class Provider(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    language = StringField()
    currency = StringField()
    
    def to_json(self, *args, **kwargs):
        data = super().to_json(*args, **kwargs)
        json_data = self.to_mongo().to_dict()
        json_data['_id'] = str(json_data['_id'])
        return json.dumps(json_data)


class ServiceArea(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    vertices = PolygonField(required=True)
    provider = ReferenceField(Provider)
    
    def to_json(self, *args, **kwargs):
        data = super().to_json(*args, **kwargs)
        json_data = self.to_mongo().to_dict()
        json_data['_id'] = str(json_data['_id'])
        json_data['provider'] = str(json_data['provider'])
        return json.dumps(json_data)
