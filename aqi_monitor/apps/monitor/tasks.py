from __future__ import absolute_import, unicode_literals
from apps.monitor.models import *
import requests
import json
from datetime import time, datetime

from celery.schedules import crontab
from celery import group
from aqi_monitor.celery import app
from . import parser
from utils import db_connector, validators
import smtplib, ssl

SENDER = "aqi.pollution.monitor@gmail.com"
PASSWORD = "byltrc54321"

app.conf.beat_schedule = {
    "send_message": {
        "task": "apps.monitor.tasks.extract_aqi",
        "schedule": crontab(minute="*/1"),
        "args": (),
    }
}


def level(aqi):
    if aqi < 46:
        return 0
    elif aqi < 51:
        return 1
    elif aqi < 96:
        return 2
    elif aqi < 101:
        return 3
    elif aqi < 146:
        return 4
    elif aqi < 151:
        return 5
    elif aqi < 156:
        return 6
    elif aqi < 201:
        return 7
    elif aqi < 291:
        return 8
    elif aqi < 300:
        return 9
    else:
        return 10


@app.task
def extract_aqi():
    regions_list = db_connector.get_cities()
    tasks_list = [send_request.s(region) for region in regions_list]
    tasks_list = group(*tasks_list).apply_async()


# FIXME
@app.task
def send_request(region):
    response = requests.get(
        f"https://api.waqi.info/feed/{region}/?token=7162b8553552c91543ed0ae44c44e59b3724a08e"
    )
    data = json.loads(response.text)["data"]
    """if validator(data):
        aqi_data_result = parse_aqi_data.parse_aqi_data(data)"""
    aqi_data_result = parser.parse_aqi_data(data)
    if validators.check_data(aqi_data_result) and validators.check_station(
        aqi_data_result
    ):
        send_message(region, aqi_data_result["aqi"])
    new_aqi = AQI()
    new_aqi.save(aqi_data_result)


@app.task
def send_message(region, current_aqi):
    message = parser.generate_message(current_aqi)
    previous_aqi = db_connector.get_latest_aqi(region)
    email_list = db_connector.get_email(region)
    if (
        previous_aqi is None
        or abs(level(previous_aqi) - level(current_aqi)) >= 2
        or ((datetime.now()).hour == 8)
        and (datetime.now()).minute <= 15
    ):
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(SENDER, PASSWORD)
            for email in email_list:
                server.sendmail(SENDER, email, message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()
