from turtle import home
from django import apps
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import url
from apps.home import views
from django.conf.urls.static import static

app_name = 'fileapp'
urlpatterns = [
    path('', views.index, name='indexname'),
    url('download', views.download_file,name='dwnfile'),
    url('filedwn', views.zipfiledown,name='dwnzipfile'),
    path('domainEntry', views.domainEntry, name = 'domainentry'),
    path('certexpirydetails', views.certexpirydetails, name = 'certexpirydetails'),
    path('crtgeneration', views.crtgeneration, name = 'crtgeneration'),
    path('reportgeneration', views.reportgenration, name = 'reportgeneration'),
    path('entry', views.entry, name = 'entry'),
    url('error',views.error,name='error')
]



