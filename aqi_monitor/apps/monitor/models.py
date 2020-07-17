from __future__ import annotations

from django.db import models
from functools import reduce


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

    def save(self, email: str, name_region: str, name: str, surname: str):
        region_ID = list(Region.objects.filter(city=name_region))[0]
        self.email = email
        self.region_ID = region_ID
        self.name = name
        self.surname = surname
        super(User, self).save()

    def __str__(self):
        return self.name + " " + self.surname


class AQI(models.Model):
    Timestamp = models.DateTimeField()
    region_ID = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="aqi_region_ID", max_length=30
    )
    PM25_index = models.IntegerField(null=True)
    PM10_index = models.IntegerField(null=True)
    NO2_index = models.IntegerField(null=True)
    CO_index = models.IntegerField(null=True)
    SO2_index = models.IntegerField(null=True)
    Ozone_index = models.IntegerField(null=True)
    final_index = models.IntegerField()
    time = models.DateTimeField()

    def save(self, aqi_data):
        region_ID = list(Region.objects.filter(city=aqi_data["city"]))[0]
        self.Timestamp = aqi_data["timestamp"]
        self.region_ID = region_ID
        self.PM25_index = aqi_data["pm25"]
        self.PM10_index = aqi_data["pm10"]
        self.SO2_index = aqi_data["so2"]
        self.CO_index = aqi_data["co"]
        self.NO2_index = aqi_data["no2"]
        self.Ozone_index = aqi_data["o3"]
        self.final_index = aqi_data["aqi"]
        self.time = aqi_data["time"]
        super(AQI, self).save()

    def __str__(self):
        return self.region_ID.city + " " + self.Timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_latest_aqi(name_region: str) -> AQI:
        """Returns the last measurement in the region

        Args:
             name_region: the city where the measurement was made
        Returns:
             The last record of the measurement
        """
        region_ID = list(Region.objects.filter(city=name_region))[0]
        aqi = list(AQI.objects.filter(region_ID=region_ID))
        if aqi:
            latest_aqi = reduce(
                lambda previous_aqi, current_aqi: previous_aqi
                if previous_aqi.Timestamp > current_aqi.Timestamp
                else current_aqi,
                aqi,
            )
            return latest_aqi
        return None
