from datetime import datetime as DT, timedelta

def out_message(aqi):
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

def time_convert(time):
    if time["tz"][0] == "+":
        hour, minute = int(time["tz"][1:3]), int(time["tz"][4:])
    else:
        hour, minute = int(time["tz"][0:3]), int("-" + time["tz"][4:])
    date = DT.strptime(time["s"], "%Y-%m-%d %H:%M:%S") + \
           timedelta(hours=hour, minutes=minute)

    return date.strftime("%Y-%m-%d %H:%M:%S")

def parse_iaqi(iaqi):
    need_aqi = ["so2", "o3", "co", "pm10", "pm25", "no2"]
    aqi = dict()
    for name, val in iaqi.items():
        if name in need_aqi:
            aqi[name] = val["v"]
    return aqi