from django.conf.urls import url
from django.urls import path
from iot import views

app_name = 'iot'

urlpatterns=[
    path('', views.index, name='iot-home'),
]