from django.urls import path,include,re_path
from . import views
urlpatterns = [
    re_path('^$',views.cart,name = 'cart'),
    re_path('^add(\d+)_(\d+)$',views.add,name = 'cart'),
    re_path('^edit(\d+)_(\d+)$',views.edit,name = 'edit'),
    re_path('^delete(\d+)$',views.delete,name = 'delete'),
    re_path('^order$',views.order,name = 'order'),
]