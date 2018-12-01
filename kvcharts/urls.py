from django.urls import re_path

from . import views
from . import handlers

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^demo/', views.demo, name='demo'),
    re_path('^put-result/', handlers.put_result, name='put_result'),
    re_path('^raise/', handlers.do_raise, name='do_raise'),
]
