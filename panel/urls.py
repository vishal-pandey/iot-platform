from django.conf.urls import url
from django.urls import path
from panel import views

app_name = 'panel'

urlpatterns=[
    path('', views.index, name='panel-home'),
    path('login/', views.login, name='panel-login'),
    path('signup/', views.signup, name='panel-signup'),
    path('signuplogin/', views.signuplogin, name='panel-signuplogin'),
    path('apps/', views.apps, name='panel-apps'),
    path('apps/devices', views.devices, name='panel-devices'),
    path('account/', views.account, name='panel-account'),
    path('logout/', views.userlogout, name='panel-logout'),
    path('connect/', views.deviceConnect, name='panel-device-connect'),
    path('select-plan/', views.selectPlan, name='panel-select-plan'),
    path('pay/', views.pay, name='panel-pay'),
    path('webhook/', views.webhook, name='webhook'),

]