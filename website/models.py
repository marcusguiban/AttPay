from django.db import models    

class Attendance(models.Model):

    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    duty_location = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=450)
    def salary_computation(self):
        # Assuming a standard workday of 8 hours
        work_hours = (self.time_out - self.time_in).total_seconds() / 3600
        computed_salary = self.salary * (work_hours / 8)
        return round(computed_salary, 2)
    # Add a property to access the computed salary
    @property
    def computed_salary(self):
        return self.salary_computation()

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")

