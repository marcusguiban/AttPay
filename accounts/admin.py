from django.contrib import admin

# Register your models here.
from .models import User, Supervisor, Employee

admin.site.register(User)
admin.site.register(Supervisor)
admin.site.register(Employee)