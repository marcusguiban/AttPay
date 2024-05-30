from django.db import models    

class Attendance(models.Model):

    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True )
    time_out = models.TimeField(auto_now=True)
    status = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    duty_location = models.CharField(max_length=50)

