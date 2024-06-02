from django.contrib import admin
from .models import Attendance, Employee, PaySlip
# Register your models here.
admin.site.register(Attendance)
admin.site.register(Employee)
admin.site.register(PaySlip)
