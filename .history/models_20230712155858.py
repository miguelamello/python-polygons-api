from mongoengine import Document, StringField, EmailField, FloatField, PointField, ReferenceField


class Provider(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    language = StringField()
    currency = StringField()


class ServiceArea(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    geo = PointField(required=True)
    provider = ReferenceField(Provider)
