from django.shortcuts import render
from pathlib import *
from django.http import HttpResponse
import random
from django.core.management.base import BaseCommand, CommandError
from apps.monitor.models import *
import random
from django.utils import timezone
from django.views.generic.list import ListView
import datetime
# Create your views here.

def addregion(request):
    reg = {}
    for i in range(ord('a'), ord('z') + 1):
        r = Region.objects.create(country = chr(i),city = chr(i))
        r.save()
    reg = {'reg' : Region.objects.all()}
    return render(request, 'addregion.html', reg)

def adduser(request):
    users = {}
    for i in range(ord('a'), ord('z') + 1):
        r = User.objects.create(email=str(chr(i) + "@mail.ru"),
                                region_ID=random.choice(Region.objects.all()), name=chr(i),
                                surname=chr(i))
        r.save()

    users = {'users' : User.objects.all()}
    return render(request, 'adduser.html', users)

def addaqi(request):
    aqis = {}
    """for i in range(27):
        r = AQI.objects.create(PM25_index=i, PM10_index=i, NO2_index=i, CO_index=i, SO2_index=i, Ozone_index=i, final_index=i, time=timezone.now(), message="")
        r.save()"""
    i = 10
    r = AQI.objects.create(PM25_index=i, PM10_index=i, NO2_index=i, CO_index=i, SO2_index=i, Ozone_index=i,
                           final_index=i, time=datetime.datetime.now(), message="")
    r.save()

    aqis = {'aqis' : AQI.objects.all()}
    return render(request, 'addaqi.html', aqis)

