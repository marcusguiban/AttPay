from django.db import models
from django.contrib.auth.models import AbstractUser

    
class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True)
    time_out = models.TimeField(auto_now=True)
    on_duty = models.BooleanField(default=True)
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


