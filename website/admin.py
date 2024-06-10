from django.contrib import admin
from .models import Attendance, PaySlip, Schedule
# Register your models here.
admin.site.register(Attendance)
admin.site.register(PaySlip)
admin.site.register(Schedule)
