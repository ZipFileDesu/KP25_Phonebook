from django.db import models

class Position(models.Model):
    position_name = models.CharField(max_length=200)

    def __str__(self):
        return self.position_name

class Region(models.Model):
    region_number = models.IntegerField(max_length=10)
    region_name = models.CharField(max_length=200)

    def __str__(self):
        return self.region_name

class Person(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    city_phone = models.CharField(max_length=200)
    ip_phone = models.CharField(max_length=200)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name