from apps.monitor.models import AQI, Region, User


def get_email(name_region: str) -> list:
    """Returns a list of users who need to send a message about air quality

    Args:
         name_region: city of users who are being sent the message
    Returns:
         A list of emails
    """
    region_ID = list(Region.objects.filter(city=name_region))[0]
    users = User.objects.filter(region_ID=region_ID)
    emails = [user.email for user in users]
    return emails


def get_aqi_index(name_region: str) -> int:
    """Returns the last aqi index value measurement in the region

    Args:
         name_region: the city where the measurement was made
    Returns:
         The last aqi index value
    """
    aqi = AQI.get_latest_aqi(name_region)
    if aqi:
        return aqi.final_index
    return None


def get_cities() -> list:
    """Returns a list of all cities in the database

    Returns:
        List of cities as a list of strings
    """
    regions = Region.objects.all()
    cities = [region.city for region in regions]
    return cities
