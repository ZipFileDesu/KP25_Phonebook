import operator
from functools import reduce

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import generic, View
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from phonebook.forms import SearchForm
from .models import Person, Department, Region, Favorite
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

    # Возвращает список работников
    def get_queryset(self):
        return Person.objects.all().filter(region_id=3)

    # Возвращает список переменных (контекстов) для вставки в HTML шаблон
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['department_list'] = Department.objects.all().order_by('id').filter(
            reduce(operator.or_, (Q(department_name__contains=x[0])
                                  for x in context['person_list'].values_list('department__department_name').exclude(
                department__isnull=True))))
        context['form'] = SearchForm(initial={'search': "", })
        context['region'] = Region.objects.all().filter(id=3)
        context['user'] = auth.get_user(self.request).username
        return context


    ''' Данный класс возвращает сотрудников данного выбранного региона. Преобразует URL адрес, исходя из выбранного региона 
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
            context['department_list'] = Department.objects.all().order_by('id').filter(
                reduce(operator.or_, (Q(department_name__contains=x[0])
                                      for x in
                                      context['person_list'].values_list('department__department_name').exclude(
                                          department__isnull=True))))
        context['form'] = SearchForm(initial={'search': "", })
        context['region'] = Region.objects.all().filter(id=self.kwargs['pk'])
        context['user'] = auth.get_user(self.request).username
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
            if form.cleaned_data['q'] == 'search':  # Если запрос не пустой, то мы возвращаем фильтрованный список работников
                filtered_persons = Person.objects.annotate(
                    search=SearchVector('full_name', 'ip_phone', 'position__position_name')) \
                    .filter(search=request.GET['q']).filter(region_id=pk)
                if filtered_persons:
                    filtered_departments = Department.objects. \
                        filter(reduce(operator.or_, (Q(department_name__contains=x[0])
                                                     for x in
                                                     filtered_persons.values_list('department__department_name').
                                      exclude(department__isnull=True))))
                else:
                    filtered_departments = None
                return render(request, 'phonebook/phonebook.html',
                              {'person_list': filtered_persons,
                               'department_list': filtered_departments,
                               'form': form,
                               'region': region,
                               'user': auth.get_user(request).username})
            elif form.cleaned_data['q'] == 'clear':  # Иначе возвращаем список всех работников
                return HttpResponseRedirect(reverse('phonebook:region', args=str(region[0].id)))


'''     Данная функция используется для фильтрации сотрудников по таким критериям: Полное имя, городской телефон,
    ip телефон, должность. Используется в ajax запросе в модальном окне, 
    возвращая переменные (person_list, department, form, region), которые вставляются в HTML шаблон'''
def searchAll(request):
    filtered_persons = Person.objects.annotate(
        search=SearchVector('full_name', 'ip_phone', 'position__position_name')) \
        .filter(search=request.GET['q'])
    if filtered_persons:
        filtered_departments = Department.objects. \
            filter(reduce(operator.or_, (Q(department_name__contains=x[0])
                                         for x in
                                         filtered_persons.values_list('department__department_name').
                          exclude(department__isnull=True))))
    else:
        return HttpResponse('По вашему запросу не было найдено ни одного сотрудника')
    return render(request, 'phonebook/searchAll.html',
                  {'person_list': filtered_persons,
                   'department_list': filtered_departments,})


''' Получить список регионов (используется в ajax запросе). Возвращает переменную region_list, которая вставляется в
HTML шаблон в модальное окно '''
def getRegionList(request):
    return render(request, 'phonebook/region.html', {'region_list': Region.objects.all()})


''' Добавляет номер в избранное. Добавляет в базу данных id пользователя, который зашёл в систему и id пользователя,
чей номер был выбран для добавления в избранное '''
def addFavorite(request):
    Favorite.objects.create(user_id=auth.get_user(request).id, favorite_number_id=request.POST['person_id'])
    return HttpResponse('')


''' Удаляет номер из избранных. Удаляет из базу данных id пользователя, который зашёл в систему и id пользователя,
чей номер был выбран для удаления из избранных '''
def removeFavorite(request):
    Favorite.objects.filter(user_id=auth.get_user(request).id, favorite_number_id=request.POST['person_id']).delete()
    return HttpResponseRedirect(reverse('phonebook:favorite-list'))


''' Получить список избранных номеров (используется в ajax запросе). Возвращает переменную favorite_list, которая
 вставляется в HTML шаблон в модальное окно '''
def getFavoriteList(request):
    favorite_list = Favorite.objects.all().filter(user_id=auth.get_user(request).id)
    if favorite_list:
        department_list = Department.objects.all().order_by('id').filter(
            reduce(operator.or_, (Q(department_name__contains=x[0])
                                  for x in favorite_list.values_list('favorite_number__department__department_name').exclude(
                favorite_number__department__isnull=True))))
        return render(request, 'phonebook/favorite.html',
                  {'favorite_list': favorite_list,
                   'department_list' : department_list})
    else:
        return HttpResponse('У вас нет избранных номеров')


# Войти в систему
def login(request, pk):
    args = {}
    args.update(csrf(request))
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponse('')
    else:
        return HttpResponse('Неверный логин или пароль!')


# Выйти из системы
def logout(request, pk):
    auth.logout(request)
    return HttpResponseRedirect(reverse('phonebook:region', args=str(pk)))
