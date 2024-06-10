from django.db import models
from django.contrib.auth.models import AbstractUser

    
class Attendance(models.Model):
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    on_duty = models.BooleanField(default=True)
    working_hours = models.CharField(max_length=50, default="0 hours 0 minutes")
    employeeID = models.CharField(max_length=100, default="Unknown")
    employee_Name = models.CharField(max_length=100, default="Unknown")  # Manually define a default value
    duty_location = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=450)
    salary_computation = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class PaySlip(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    employeeID = models.CharField(max_length=100, default="Unknown")
    employee_name = models.CharField(max_length=100)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

class Schedule(models.Model):
    employeeID = models.CharField(max_length=20)
    monday_start = models.TimeField(null=True, blank=True)
    monday_end = models.TimeField(null=True, blank=True)
    tuesday_start = models.TimeField(null=True, blank=True)
    tuesday_end = models.TimeField(null=True, blank=True)
    wednesday_start = models.TimeField(null=True, blank=True)
    wednesday_end = models.TimeField(null=True, blank=True)
    thursday_start = models.TimeField(null=True, blank=True)
    thursday_end = models.TimeField(null=True, blank=True)
    friday_start = models.TimeField(null=True, blank=True)
    friday_end = models.TimeField(null=True, blank=True)
    saturday_start = models.TimeField(null=True, blank=True)
    saturday_end = models.TimeField(null=True, blank=True)
    sunday_start = models.TimeField(null=True, blank=True)
    sunday_end = models.TimeField(null=True, blank=True)

