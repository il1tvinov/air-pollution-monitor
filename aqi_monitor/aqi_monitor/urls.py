
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("monitor/", include('apps.monitor.urls')),
    path('admin/', admin.site.urls)
]