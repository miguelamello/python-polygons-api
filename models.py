from mongoengine import Document, StringField, EmailField, FloatField, PolygonField, ReferenceField


class Provider(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    language = StringField()
    currency = StringField()


class ServiceArea(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    vertices = PolygonField(required=True)
    provider = ReferenceField(Provider)
