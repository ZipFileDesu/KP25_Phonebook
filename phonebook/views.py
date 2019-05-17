from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Person

'''def index(request):
    return HttpResponse("<p>Test page 1 2 3, тестовая страница 1 2 3</p>")'''

class IndexView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        return Person.objects.all()
