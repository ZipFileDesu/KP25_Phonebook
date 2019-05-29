import operator
from functools import reduce

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, request, HttpResponseRedirect
from phonebook.forms import SearchForm
from .models import Person, Department
from django.contrib.postgres.search import SearchVector
import numpy as np

''' Класс общих представлений generic views, который берёт из базы данных данные и вставляет нам в HTML страницу '''


'''     Здесь планировалось использовать фреймворки Haystrack и Whoosh для поиска нескольких строк таблицы или таблиц 
    по БД, но Haystrack (считай обёртка) уж больно кривой и к тому же он явно заточен под старую версию Django. 
    Тем более, в случае с БД Postrgresql, уже существует нормальная реализация поиска в самой БД, поэтому особого смысла
    встраивать левый фреймворк для поиска по бд нет '''


'''     Данный класс ListView используется для отображения информации, которая берётся из БД, возвращая переменные 
    (или же контекст person_list, department, form), которые вставляются в HTML шаблон (например: kadastr/phonebook)'''
class IndexView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    # Возвращает список работников
    def get_queryset(self):
        return Person.objects.all()

    # Возвращает список переменных (контекстов) для вставки в HTML шаблон
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all().order_by('id')
        context['form'] = SearchForm(initial={'search': "", })
        return context


'''     Данная функция используется для фильтрации сотрудников по таким критериям: Полное имя, городской телефон, 
    ip телефон, должность. Также преобразует URL адрес, исходя из запроса или вбитых данных в форму 
    (например kadastr/phonebook/searc/q=danil), возвращая переменные (person_list, department, form), 
     которые вставляются в HTML шаблон'''
def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['q']:      # Если запрос не пустой, то мы возвращаем фильтрованный список работников
                filtered_persons = Person.objects.annotate(
                    search=SearchVector('full_name', 'ip_phone', 'position__position_name')) \
                    .filter(search__icontains=request.GET['q'])
                if filtered_persons:
                    filtered_departments = Department.objects.\
                        filter(reduce(operator.or_, (Q(department_name__contains=x[0])
                                        for x in filtered_persons.values_list('department__department_name').
                                    exclude(department__isnull=True))))
                else:
                    filtered_departments = None
                return render(request, 'phonebook/phonebook.html',
                              {'person_list': filtered_persons,
                               'departments': filtered_departments,
                               'form': form})
            else:       # Иначе возвращаем список всех работников
                return render(request, 'phonebook/phonebook.html',
                              {'person_list': Person.objects.all(),
                               'departments': Department.objects.all().order_by('id'),
                               'form': form})
