from django.db import models


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
    PM25_index = models.IntegerField(null=True)
    PM10_index = models.IntegerField(null=True)
    NO2_index = models.IntegerField(null=True)
    CO_index = models.IntegerField(null=True)
    SO2_index = models.IntegerField(null=True)
    Ozone_index = models.IntegerField(null=True)
    final_index = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.region_ID.city + " " + self.time.strftime("%Y-%m-%d %H:%M:%S")
