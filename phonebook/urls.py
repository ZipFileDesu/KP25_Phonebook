from django.urls import path

from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('<string:search>', views.Search.as_view(), name='search')
]