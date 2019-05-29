from django.db import models


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


# В каком филиале сотрудник числится
class BranchOffice(models.Model):
    branch_office_region_number = models.IntegerField()
    branch_office_name = models.CharField(max_length=200)

    def __str__(self):
        return self.branch_office_name


# Информация о самом сотруднике
class Person(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    city_phone = models.CharField(max_length=200)
    ip_phone = models.CharField(max_length=200)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, default=None)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.PROTECT, null=True, default=None)

    def __str__(self):
        return self.full_name
