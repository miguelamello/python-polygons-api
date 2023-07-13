from django.db import models

class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class ServiceArea(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    geojson = models.JSONField()

    def __str__(self):
        return self.name
