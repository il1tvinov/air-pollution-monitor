from pytz import utc
from datetime import datetime


def message_about_air_quality(aqi: int) -> str:
    """Determines the air quality and returns the corresponding message

    Args:
        aqi: Air quality index

    Returns:
        Message about air quality
    """
    if aqi < 51:
        return ""
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


def parse_iaqi(iaqi: dict) -> dict:
    """Retrieves the values of the required air parameters

    Args:
         iaqi: A dictionary with all parameters of air

    Returns:
         A dictionary with the required air parameters
    """
    required_attributes = ["so2", "o3", "co", "pm10", "pm25", "no2"]
    aqi = {attr: iaqi.get(attr).get("v", 0) for attr in required_attributes}
    return aqi


def parse_aqi_data(data: dict) -> dict:
    """Returns data to the type required for writing to the database

    Args:
         data: A dictionary with all measurement results

    Returns:
         A dictionary with the required parameters for the database
    """
    aqi = parse_iaqi(data["iaqi"])
    result = {"id_region": data["idx"],
              "aqi": data["aqi"],
              "message": message_about_air_quality(data["aqi"]),
              "time": time_convert_to_utc(data["time"])}
    result.update(aqi)
    return result
