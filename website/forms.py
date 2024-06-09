
from django import forms
from .models import Attendance

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