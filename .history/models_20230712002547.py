from mongoengine import Document, StringField, EmailField, FloatField, PointField, ReferenceField


class Provider(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField(required=True)
    language = StringField()
    currency = StringField()


class ServiceArea(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    geojson = PointField(required=True)
    provider = ReferenceField(Provider)
