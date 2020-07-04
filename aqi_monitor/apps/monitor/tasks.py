from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from aqi_monitor.celery import app
import requests
import json

app.conf.beat_schedule = \
    {"send_message": {
        "task": "apps.monitor.tasks.get_aqi",
        "schedule": crontab(minute="*/1"),
        "args": (),
    }}


@app.task
def get_aqi():
    region = "saratov"
    response = requests.get(
        "https://api.waqi.info/feed/" + region + "/?token=7162b8553552c91543ed0ae44c44e59b3724a08e")
    result = json.loads(response.text)
    print(result)