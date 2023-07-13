from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)


class ServiceArea(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    geojson = models.GeometryField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
