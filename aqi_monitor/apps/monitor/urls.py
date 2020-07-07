from django.conf.urls import url
from . import views
from django.urls import path, include

urlpatterns = [
    path('region', views.addregion, name='addregion'),
    path('aqi', views.addaqi, name='addaqi'),
    path('user', views.adduser, name='adduser'),
]