from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Person, Department
from django.contrib.postgres.search import SearchVector

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
        return context

''' !!! Переделать в ListView, поскольку здесь у нас в данном случае происходит поиск, а не берётся конкретный первичный ключ из бд '''
''' Данный класс DetailView используется для URL преобразования (например: kadastr/phonebook/person_name=danil)'''
class SearchView(generic.DetailView):
    template_name = 'phonebook/search.html'
    model = Person
    context_object_name = ''

    def get_queryset(self):
        sqs = Person.objects.annotate(search=SearchVector('full_name','ip_phone', 'position__position_name'))\
            .filter(search__icontains=self.kwargs['search'])
        return sqs