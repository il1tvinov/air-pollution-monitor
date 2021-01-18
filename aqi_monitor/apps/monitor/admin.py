from django.contrib import admin
from apps.monitor.models import AQI, User, Region

admin.site.register(User)
admin.site.register(Region)
admin.site.register(AQI)
