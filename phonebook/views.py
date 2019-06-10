import operator
from functools import reduce

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, request, HttpResponseRedirect
from phonebook.forms import SearchForm
from .models import Person, Department, Region
from django.contrib.postgres.search import SearchVector
import numpy as np

''' Класс общих представлений generic views, который берёт из базы данных данные и вставляет нам в HTML страницу '''


'''     Здесь планировалось использовать фреймворки Haystrack и Whoosh для поиска нескольких строк таблицы или таблиц 
    по БД, но Haystrack (считай обёртка) уж больно кривой и к тому же он явно заточен под старую версию Django. 
    Тем более, в случае с БД Postrgresql, уже существует нормальная реализация поиска в самой БД, поэтому особого смысла
    встраивать левый фреймворк для поиска по бд нет '''


'''     Данный класс ListView используется для отображения информации, которая берётся из БД, возвращая переменные 
    (или же контекст person_list, department, form, region), 
    которые вставляются в HTML шаблон (например: kadastr/phonebook). 
    Он рендерит страницу региона ЦА ФГБУ '''
class IndexView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return render(request, 'phonebook/region.html',{'entry_list': Region.objects.all()})
        else:
            return super().dispatch(request, *args, **kwargs)

    # Возвращает список работников
    def get_queryset(self):
        return Person.objects.all().filter(region_id=3)

    # Возвращает список переменных (контекстов) для вставки в HTML шаблон
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all().order_by('id').filter(reduce(operator.or_, (Q(department_name__contains=x[0])
                                        for x in context['person_list'].values_list('department__department_name').exclude(department__isnull=True))))
        context['form'] = SearchForm(initial={'search': "", })
        context['region'] = Region.objects.all().filter(id=3)
        return context

    '''     Данная функция используется для фильтрации сотрудников по таким критериям: Полное имя, городской телефон,
    ip телефон, должность. Также преобразует URL адрес, исходя из запроса или вбитых данных в форму 
    (например kadastr/phonebook/1/search/q=danil), возвращая переменные (person_list, department, form, region), 
     которые вставляются в HTML шаблон'''
def search(request, pk):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            region = Region.objects.all().filter(id=pk)
            if form.cleaned_data['q']:      # Если запрос не пустой, то мы возвращаем фильтрованный список работников
                filtered_persons = Person.objects.annotate(
                    search=SearchVector('full_name', 'ip_phone', 'position__position_name')) \
                    .filter(search=request.GET['q']).filter(region_id=pk)
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
                               'form': form,
                               'region': region})
            else:       # Иначе возвращаем список всех работников
                return HttpResponseRedirect(reverse('phonebook:region',args=str(region[0].id)))

''' Данный класс используется для выбора региона. Преобразует URL адрес, исходя из выбранного региона 
(например: kadastr/phonebook/1), возвращая переменные (person_list, department, form, region), 
которые вставляются в HTML шаблон '''
class RegionView(generic.ListView):
    template_name = 'phonebook/phonebook.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        return Person.objects.all().filter(region_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(RegionView, self).get_context_data(**kwargs)
        if context['person_list']:
            context['departments'] = Department.objects.all().order_by('id').filter(reduce(operator.or_, (Q(department_name__contains=x[0])
                                        for x in context['person_list'].values_list('department__department_name').exclude(department__isnull=True))))
        context['form'] = SearchForm(initial={'search': "", })
        context['region'] = Region.objects.all().filter(id=self.kwargs['pk'])
        return context
