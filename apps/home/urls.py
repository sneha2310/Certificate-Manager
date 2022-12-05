from turtle import home
from django import apps
from django.conf import settings
from django.urls import path, re_path
# from django.urls import url
from apps.home import views
from django.conf.urls.static import static

app_name = 'fileapp'
urlpatterns = [
    path('', views.index, name='indexname'),
    re_path('download', views.download_file,name='dwnfile'),
    re_path('filedwn', views.zipfiledown,name='dwnzipfile'),
    path('domainEntry', views.domainEntry, name = 'domainentry'),
    path('certexpirydetails', views.certexpirydetails, name = 'certexpirydetails'),
    path('crtgeneration', views.crtgeneration, name = 'crtgeneration'),
    path('reportgeneration', views.reportgenration, name = 'reportgeneration'),
    path('entry', views.entry, name = 'entry'),
    re_path('error',views.error,name='error')
]



