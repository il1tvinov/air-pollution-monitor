from __future__ import absolute_import, unicode_literals
import time
from aqi_monitor.celery import app


@app.task(bind=True)
def celery_task(self, counter):
    time.sleep(3)
    return '{} Done!'.format(counter)