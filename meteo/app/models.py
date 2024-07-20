from django.db import models


# Create your models here.

class City(models.Model):
    """
    - храним координаты городов
    """
    city = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
