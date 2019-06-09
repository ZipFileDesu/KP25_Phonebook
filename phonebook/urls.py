from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.RegionView.as_view(), name='region'),
    re_path(r'^(?P<pk>[0-9]+)/search/$', views.search, name='search'),
    #re_path(r'^search/$<str:search>', views.SeachView.as_view, name='search')
]
