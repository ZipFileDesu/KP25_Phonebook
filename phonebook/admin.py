from django.contrib import admin
from .models import Person, Position, Department, Branch_Office

admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Branch_Office)
