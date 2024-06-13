
from django import forms
from .models import Attendance, PaySlip

class AttendanceForm(forms.ModelForm):
    employeeID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "ID", "class": "form-control", "readonly": "readonly"}), label="")
    employee_Name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Name", "class": "form-control", "readonly": "readonly"}), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Duty Location", "class": "form-control"}), label="")
    date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder": "Date", "class": "form-control", "type": "date", "readonly": "readonly"}), label="")
    time_in = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time In", "class": "form-control", "type": "time", "readonly": "readonly"}), label="")
    
    class Meta:
        model = Attendance
        exclude = ("user", "on_duty", "salary", "salary_computation", "working_hours","time_out")


class AttendanceFormAdmin(forms.ModelForm):
    employeeID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "ID", "class": "form-control", }), label="")
    employee_Name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Name", "class": "form-control", }), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Duty Location", "class": "form-control"}), label="")
    salary = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Salary", "class": "form-control"}), label="")
    salary_computation = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Salary Computation", "class": "form-control"}), label="")
    working_hours = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Working Hours", "class": "form-control"}), label="")
    date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder": "Date", "class": "form-control", "type": "date"}), label="")
    time_in = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time In", "class": "form-control", "type": "time"}), label="")
    time_out = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time Out", "class": "form-control", "type": "time"}), label="")
    class Meta:
        model = Attendance
        exclude = ("user",)
class TimeOutForm(forms.ModelForm):
    working_hours = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(attrs={ "class": "form-control", "readonly": "readonly"}),
        label="Working Hours:"
    )
    
    salary = forms.DecimalField(
        required=True,
        widget=forms.widgets.TextInput(attrs={ "class": "form-control", "readonly": "readonly"}),
        label="Salary:"
    )
    salary_computation = forms.DecimalField(
        required=True,
        widget=forms.widgets.TextInput(attrs={ "class": "form-control", "readonly": "readonly"}),
        label="Salary Computation:"
    )
    time_out = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time Out", "class": "form-control", "type": "time", "readonly": "readonly"}), label="")

    class Meta:
        model = Attendance
        exclude = ("user","first_name", "last_name","email","duty_location", "employeeID", "on_duty", "employee_Name", "date", "time_in")


class EditAttendanceFormAdmin(forms.ModelForm):
    employeeID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "ID", "class": "form-control"}), label="")
    employee_Name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Name", "class": "form-control"}), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Duty Location", "class": "form-control"}), label="")
    date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder": "Date", "class": "form-control", "type": "date"}), label="")
    time_in = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time In", "class": "form-control", "type": "time"}), label="")
    time_out = forms.TimeField(required=True, widget=forms.widgets.TimeInput(attrs={"placeholder": "Time Out", "class": "form-control", "type": "time"}), label="")
    working_hours = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Working Hours", "class": "form-control"}), label="")
    salary = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Salary", "class": "form-control"}), label="")
    salary_computation = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Salary Computation", "class": "form-control"}), label="")

    class Meta:
        model = Attendance
        fields = "__all__"

class PayslipForm(forms.ModelForm):
    employeeID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "ID", "class": "form-control"}), label="Employee ID")
    employee_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Name", "class": "form-control"}), label="Employee Name")
    date_start = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder": "Start Date", "class": "form-control", "type": "date"}), label="Start Date")
    date_end = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder": "End Date", "class": "form-control", "type": "date"}), label="End Date")
    paid = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Paid"
    )
    total_salary = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Total Salary", "class": "form-control"}), label="Total Salary")

    class Meta:
        model = PaySlip
        fields = "__all__"
        

from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    employeeID = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Employee ID", "class": "form-control"}), 
        label="Employee ID"
    )
    
    monday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Monday Start", "class": "form-control", "type": "time"}), 
        label="Monday Start"
    )
    monday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Monday End", "class": "form-control", "type": "time"}), 
        label="Monday End"
    )
    tuesday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Tuesday Start", "class": "form-control", "type": "time"}), 
        label="Tuesday Start"
    )
    tuesday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Tuesday End", "class": "form-control", "type": "time"}), 
        label="Tuesday End"
    )
    wednesday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Wednesday Start", "class": "form-control", "type": "time"}), 
        label="Wednesday Start"
    )
    wednesday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Wednesday End", "class": "form-control", "type": "time"}), 
        label="Wednesday End"
    )
    thursday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Thursday Start", "class": "form-control", "type": "time"}), 
        label="Thursday Start"
    )
    thursday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Thursday End", "class": "form-control", "type": "time"}), 
        label="Thursday End"
    )
    friday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Friday Start", "class": "form-control", "type": "time"}), 
        label="Friday Start"
    )
    friday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Friday End", "class": "form-control", "type": "time"}), 
        label="Friday End"
    )
    saturday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Saturday Start", "class": "form-control", "type": "time"}), 
        label="Saturday Start"
    )
    saturday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Saturday End", "class": "form-control", "type": "time"}), 
        label="Saturday End"
    )
    sunday_start = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Sunday Start", "class": "form-control", "type": "time"}), 
        label="Sunday Start"
    )
    sunday_end = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={"placeholder": "Sunday End", "class": "form-control", "type": "time"}), 
        label="Sunday End"
    )

    class Meta:
        model = Schedule
        fields = "__all__"
