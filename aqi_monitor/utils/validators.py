def check_station(aqi_response: dict) -> bool:
    """ This function checks whether the station is functioning

    Args:
        aqi_response: data from the AQI service in the form of a dictionary

    Returns:
        A response in the form of a Boolean value
    """
    if aqi_response.get("status") == "error":
        return False
    return True


def check_data(aqi_response: dict):
    """ This function checks whether the station has data.

    Args:
        aqi_response: data from the AQI service in the form of a dictionary

    Returns:
        A response in the form of a Boolean value
    """
    data = aqi_response.get("data")
    if (
        not isinstance(data.get("aqi"), int)
        or data.get("time").get("s") == ""
        or data.get("time").get("tz") == ""
    ):
        return False
    return True
