from django.contrib.auth.models import User
from django.db import models
from django.contrib import auth

from main import settings

# Должность сотрудника
class Position(models.Model):
    position_name = models.CharField(max_length=200)

    def __str__(self):
        return self.position_name


''' В каком отделе филиала сотрудник работает (например, сотрудник числится в филиале Приморского края и работает
в отделе подготовки кадров) '''
class Department(models.Model):
    department_name = models.CharField(max_length=200)

    def __str__(self):
        return self.department_name


# Город
class City(models.Model):
    city_name = models.CharField(max_length=200)
    timezone = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.city_name


# В каком филиале сотрудник числится
class Region(models.Model):
    region_name = models.CharField(max_length=200)
    city_id = models.ForeignKey(City, on_delete=models.PROTECT, null=True, default=None)

    def __str__(self):
        return self.region_name

# Информация о самом сотруднике
class Person(models.Model):
    auth_user = models.ForeignKey(User, null=True, default=None, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, default=None)
    city_phone = models.CharField(max_length=200, null=True, default=None)
    ip_phone = models.CharField(max_length=200, null=True, default=None)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, default=None)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, default=None)
    room = models.CharField(max_length=10, null=True, default=None)

    def __str__(self):
        return self.full_name

# Избранные номера для каждого сотрудника (работают только в том случае, если пользователь залогинился)
class Favorite(models.Model):
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    favorite_number = models.ForeignKey(Person, null=True, default=None, on_delete=models.CASCADE)