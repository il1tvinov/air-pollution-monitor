from __future__ import absolute_import, unicode_literals

import requests
import json

from celery.schedules import crontab
from celery import group
from aqi_monitor.celery import app
from . import parse_aqi_data


app.conf.beat_schedule = \
    {"send_message": {
        "task": "apps.monitor.tasks.extract_aqi",
        "schedule": crontab(minute="*/1"),
        "args": (),
    }}

@app.task
def extract_aqi():
    regions_list = ["moscow", "paris", "new%20york", "saratov", "berlin", "tokyo"]
    tasks_list = [send_request.s(i) for i in regions_list]
    tasks_list = group(*tasks_list).apply_async()


@app.task
def send_request(region):
    response = requests.get(
        f"https://api.waqi.info/feed/{region}/?token=d03d6e3baa62248fd0f86b3df1c70b211ed08f35")
    data = json.loads(response.text)["data"]
    aqi_data_result = parse_aqi_data.parse_aqi_data(data)
