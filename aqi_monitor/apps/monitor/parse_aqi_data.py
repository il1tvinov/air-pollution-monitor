from pytz import utc
from datetime import datetime


def validator(all_data: dict) -> bool:
    """ The function reports whether the service provided correct data
        for processing or not

    Args:
        all_data: data from the AQI service in the form of a dictionary

    Returns:
        A response in the form of a Boolean value
    """
    if all_data.get("status") == "error":
        return False
    data = all_data.get("data")
    if (
        not isinstance(data.get("aqi"), int)
        or data.get("time").get("s") == ""
        or data.get("time").get("tz") == ""
    ):
        return False
    return True


def message_about_air_quality(aqi: int) -> str:
    """Determines the air quality and returns the corresponding message

    Args:
        aqi: Air quality index

    Returns:
        Message about air quality
    """
    if aqi < 51:
        return "Good air"
    elif aqi < 101:
        return "Air quality is acceptable"
    elif aqi < 151:
        return "Members of sensitive groups may experience health effects"
    elif aqi < 201:
        return "Everyone may begin to experience health effects"
    elif aqi < 301:
        return "Health warnings of emergency conditions"
    else:
        return "Health alert: everyone may experience more serious health effects"


def time_convert_to_utc(time: dict) -> datetime:
    """Converts time to utc

    Args:
         time: Date, time, and timezone in dict format

    Returns:
         Datetime in utc
    """
    time_with_tz = time["s"] + " " + time["tz"][0:3] + time["tz"][4:]
    date = datetime.strptime(time_with_tz, "%Y-%m-%d %H:%M:%S %z")
    return date.astimezone(utc)


def parse_aqi_data(data: dict, city: str) -> dict:
    """Returns data to the type required for writing to the database

    Args:
         data: A dictionary with all measurement results and city
         in format string
    Returns:
         A dictionary with the required parameters for the database
    """
    iaqi = data.get("iaqi")
    required_attributes = ["so2", "o3", "co", "pm10", "pm25", "no2"]
    aqi = {
        attr: iaqi.get(attr, None).get("v", 0) if iaqi.get(attr) else None
        for attr in required_attributes
    }
    result = {
        "city": city,
        "aqi": data.get("aqi"),
        "time": time_convert_to_utc(data.get("time")),
    }
    result.update(aqi)
    return result
