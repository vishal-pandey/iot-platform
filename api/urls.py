from django.conf.urls import url
from django.urls import path
from api import views

app_name = 'api'

urlpatterns=[
    path('', views.index, name='api'),
    path('apps/', views.apps, name='apps'),
    path('apps/<k>/', views.apps, name='apps'),
    path('devices/', views.devices, name='devices'),
    path('devices/<k>/', views.devices, name='devices'),

]