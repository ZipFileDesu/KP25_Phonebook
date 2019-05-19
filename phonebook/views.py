from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Person, Department

'''def index(request):
    return HttpResponse("<p>Test page 1 2 3, тестовая страница 1 2 3</p>")'''

class IndexView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        return Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all().order_by('id')
        # Add any other variables to the context here
        ...
        return context