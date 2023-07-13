from mongoengine import Document, fields

class Provider(Document):
    name = fields.StringField(max_length=100)
    email = fields.EmailField()
    phone_number = fields.StringField(max_length=20)
    language = fields.StringField(max_length=50)
    currency = fields.StringField(max_length=10)

    def __str__(self):
        return self.name

class ServiceArea(Document):
    name = fields.StringField(max_length=100)
    price = fields.DecimalField(precision=2)
    geojson = fields.DictField()

    def __str__(self):
        return self.name
