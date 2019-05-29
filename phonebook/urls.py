from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^search/$', views.search),
    # path('<str:q>', views.Search)
]
