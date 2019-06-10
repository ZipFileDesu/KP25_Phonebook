from django.contrib import admin
from .models import Person, Position, Department, City, Region

admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Region)
admin.site.register(City)
