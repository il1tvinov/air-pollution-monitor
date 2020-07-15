from functools import reduce

import apps.monitor.models as models


def save_region_in_db(country: str, city: str):
    region = models.Region(country=country, city=city)
    region.save()


def save_aqi_in_db(aqi_data: dict):
    aqi = models.AQI()
    region = models.Region.objects.filter(aqi_data["city"])[0]
    aqi.region_ID = region
    aqi.PM25_index = aqi_data["pm25"]
    aqi.PM10_index = aqi_data["pm10"]
    aqi.SO2_index = aqi_data["so2"]
    aqi.CO_index = aqi_data["co"]
    aqi.NO2_index = aqi_data["no2"]
    aqi.Ozone_index = aqi_data["o3"]
    aqi.final_index = aqi_data["aqi"]
    aqi.time = aqi_data["time"]
    aqi.message = aqi_data["message"]
    aqi.save()


def save_user_in_db(email: str, name_region: str, name: str, surname: str):
    region = models.Region.objects.filter(city=name_region)[0]
    user = models.User(email=email, region_ID=region, name=name, surname=surname)
    user.save()


def get_email(name_region: str) -> list:
    """Returns a list of users who need to send a message about air quality

    Args:
         name_region: city of users who are being sent the message
    Returns:
         A list of emails
    """
    region = list(models.Region.objects.filter(city=name_region))[0]
    users = models.User.objects.filter(region)
    all_email = [user.email for user in users]
    return all_email


def get_latest_aqi(name_region: str) -> models.AQI:
    """Returns the last measurement in the region

    Args:
         name_region: the city where the measurement was made
    Returns:
         The last record of the measurement
    """
    region = models.Region.objects.filter(city=name_region)[0]
    aqi = list(models.AQI.objects.filter(region_ID=region))
    if aqi:
        latest_aqi = reduce(lambda x, y: x if x.time > y.time else y, aqi)
        return latest_aqi
    return None


def get_aqi_index(name_region: str) -> int:
    """Returns the last aqi index value measurement in the region

    Args:
         name_region: the city where the measurement was made
    Returns:
         The last aqi index value
    """
    aqi = get_latest_aqi(name_region)
    if aqi:
        return aqi.final_index
    return None


def get_aqi_message(name_region: str) -> str:
    """Returns a message about the air quality in the last measurement

    Args:
         name_region: the city where the measurement was made
    Returns:
         The message about air quality
    """
    aqi = get_latest_aqi(name_region)
    if aqi:
        return aqi.message
    return None


def get_all_regions() -> list:
    """Returns a list of all cities in the database

    Returns:
        List of cities as a list of strings
    """
    all_regions = models.Region.objects.all()
    all_name_region = [region.city for region in all_regions]
    return all_name_region
