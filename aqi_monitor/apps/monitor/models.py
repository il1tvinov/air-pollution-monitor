from django.db import models
from django.utils import timezone
import datetime

class Region(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

class User(models.Model):
    email = models.CharField(max_length=30)
    region_ID = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='user_region_ID',  max_length=30)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

class AQI(models.Model):
    region_ID = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='aqi_region_ID', max_length=30)
    PM25_index = models.IntegerField()
    PM10_index = models.IntegerField()
    NO2_index = models.IntegerField()
    CO_index = models.IntegerField()
    SO2_index = models.IntegerField()
    Ozone_index = models.IntegerField()
    final_index = models.IntegerField()
    time = models.DateTimeField()
    message = models.CharField(max_length=200)


