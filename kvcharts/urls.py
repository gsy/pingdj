from django.urls import re_path

from . import views
from . import handlers

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^demo/', views.demo, name='demo'),
    re_path(r'^method/([A-Za-z0-9_-]+)/$', views.detail, name='detail'),
    re_path('^demo_with_children/', views.demo_with_children, name='demo_with_children'),
    re_path('^put-result/', handlers.put_result, name='put_result'),
    re_path('^raise/', handlers.do_raise, name='do_raise'),
]
