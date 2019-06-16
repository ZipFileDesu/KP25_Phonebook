from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('region-list/', views.getRegionList, name='region-list'),
    path('favorite-list/', views.getFavoriteList, name='favorite-list'),
    path('add-favorite/', views.addFavorite, name='add-favorite'),
    path('remove-favorite/', views.removeFavorite, name='remove-favorite'),
    path('<int:pk>/', views.RegionView.as_view(), name='region'),
    path('<int:pk>/login/', views.login, name='login'),
    path('<int:pk>/logout/', views.logout, name='logout'),
    path('search-all/', views.searchAll, name='search-all'),
    re_path(r'^(?P<pk>[0-9]+)/search/$', views.search, name='search'),
    #re_path(r'^search/$<str:search>', views.SeachView.as_view, name='search')
]
