from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, request, HttpResponseRedirect
from phonebook.forms import SearchForm
from .models import Person, Department
from django.contrib.postgres.search import SearchVector
import numpy as np

'''def index(request):
    return HttpResponse("<p>Test page 1 2 3, тестовая страница 1 2 3</p>")'''

''' Класс общих представлений generic views, который берёт из базы данных данные и вставляет нам в HTML страницу '''

''' Можно было бы сделать всё по классике, беря сначала с базы данных данные а потом использовать функцию render(),
    но с классами общих представлений это всё делается куда проще + сокращается большая часть кода '''

''' Здесь планировалось использовать фреймворки Haystrack и Whoosh для поиска нескольких строк таблицы или таблиц по БД, 
    но Haystrack (считай обёртка) уж больно кривой и к тому же он явно заточен под старую версию Django. Тем более,
    в случае с БД Postrgresql, уже существует нормальная реализация поиска в самой БД, поэтому особого смысла
    встраивать левый фреймворк для поиска по бд нет '''

''' Данный класс ListView используется для отображения информации, которая берётся из БД и потом вставляется в HTML
    страницу (например: kadastr/phonebook)'''
class IndexView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        return Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all().order_by('id')
        context['form'] = SearchForm(initial={'search': "",})
        return context


''' Данный класс используется для URL преобразования (например: kadastr/phonebook/person_name=danil)'''
'''def Search(request):
    if request.method == 'GET':
        return render(request, 'phonebook/search.html',
                  {'person_list': Person.objects.annotate(search=SearchVector('full_name','ip_phone', 'position__position_name'))\
            .filter(search__icontains=request.GET['q'])})'''

''' Нужно учитывать тот случай, что строка может быть пустой '''
def Search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['q']:
                return render(request, 'phonebook/search.html',
                    {'person_list': Person.objects.annotate(
                        search=SearchVector('full_name', 'ip_phone', 'position__position_name')) \
                        .filter(search__icontains=request.GET['q']),
                     'form': form})
            else:
                return render(request, 'phonebook/phonebook.html',
                              {'departments': Department.objects.all().order_by('id'),
                               'person_list': Person.objects.all(),
                               'form': form})