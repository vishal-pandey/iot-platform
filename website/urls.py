from django.conf.urls import url
from django.urls import path
from website import views

app_name = 'website'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # url(r'',views.index, name='index'),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    # path('services', views.services, name='services'),
    # path('courses', views.courses, name='courses'),
    # path('teacher', views.teacher, name='teacher'),
    path('contact', views.contact, name='contact'),
    # path('privacy', views.ppolicy, name='privacy')
]