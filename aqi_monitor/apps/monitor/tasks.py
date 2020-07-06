from __future__ import absolute_import, unicode_literals

import requests
import json

from celery.schedules import crontab
from aqi_monitor.celery import app
from . import function_for_task as fun


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
        f"https://api.waqi.info/feed/{region}/?token=7162b8553552c91543ed0ae44c44e59b3724a08e")
    data = json.loads(response.text)["data"]
    idx = {"id_region": data["idx"]}
    aqi_val = {"aqi": data["aqi"]}
    aqi = fun.parse_iaqi(data["iaqi"])
    message = {"message": fun.out_message(aqi_val["aqi"])}
    time = {"time": fun.time_convert(data["time"])}
    result = dict()
    result.update(aqi_val)
    result.update(idx)
    result.update(aqi)
    result.update(time)
    result.update(message)