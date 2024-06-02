from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Consider encrypting passwords
    email = models.EmailField(max_length=100)
    contact_number = models.CharField(max_length=15)
    deployment = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=450)
        # Provide custom related names for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_set',
        related_query_name='employee',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_set',
        related_query_name='employee',
        blank=True,
        verbose_name='user permissions',
    )
    
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


