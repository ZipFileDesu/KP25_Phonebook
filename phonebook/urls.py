from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/<str:search>', views.Search, name='search'),
    #url(r'^search/$', views.Search),
]