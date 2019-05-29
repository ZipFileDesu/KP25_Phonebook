from django.contrib import admin
from .models import Person, Position, Department, BranchOffice

admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(BranchOffice)
