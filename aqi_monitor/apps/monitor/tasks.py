from __future__ import absolute_import, unicode_literals

import requests
import json

from celery.schedules import crontab
from aqi_monitor.celery import app
from . import parse_aqi_data


app.conf.beat_schedule = \
    {"send_message": {
        "task": "apps.monitor.tasks.get_aqi",
        "schedule": crontab(minute="*/15"),
        "args": (),
    }}


@app.task
def get_aqi():
    region = "moscow"
    response = requests.get(
        f"https://api.waqi.info/feed/{region}/?token=7162b8553552c91543ed0ae44c44e59b3724a08e")
    data = json.loads(response.text)["data"]
    aqi_data_result = parse_aqi_data.parse_aqi_data(data)