from django.db import models
from django.utils import timezone
import datetime


class Region(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.country + ", " + self.city


class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    region_ID = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="user_region_ID", max_length=30
    )
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return self.name + " " + self.surname


class AQI(models.Model):
    region_ID = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="aqi_region_ID", max_length=30
    )
    PM25_index = models.IntegerField()
    PM10_index = models.IntegerField()
    NO2_index = models.IntegerField()
    CO_index = models.IntegerField()
    SO2_index = models.IntegerField()
    Ozone_index = models.IntegerField()
    final_index = models.IntegerField()
    time = models.DateTimeField()
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.region_ID.city + " " + self.time.strftime("%Y-%m-%d %H:%M:%S")
