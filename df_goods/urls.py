from django.contrib import admin
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    re_path('^$',views.index,name = 'index'),
    re_path('list(\d+)_(\d+)_(\d+)',views.goodlist,name = 'goodlist'),
    re_path('^(\d+)$',views.detail,name='detail')
]