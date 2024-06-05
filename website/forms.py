
from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    employeeID = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "ID", "class": "form-control", "readonly": "readonly"}), label="")
    employee_Name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Name", "class": "form-control", "readonly": "readonly"}), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Duty Location", "class": "form-control"}), label="")

    class Meta:
        model = Attendance
        exclude = ("user", "on_duty", "salary", "salary_computation")

class TimeOutForm(forms.ModelForm):
    
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


    class Meta:
        model = Attendance
        exclude = ("user","first_name", "last_name","email","duty_location", "employeeID", "on_duty", "employee_Name")


class EditAttendanceFormAdmin(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        widgets = {
            'employeeID': forms.TextInput(attrs={"placeholder": "ID", "class": "form-control"}),
            'employee_Name': forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}),
            'duty_location': forms.TextInput(attrs={"placeholder": "Duty Location", "class": "form-control"}),
            'on_duty': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'salary': forms.NumberInput(attrs={"placeholder": "Salary", "class": "form-control"}),
            'salary_computation': forms.NumberInput(attrs={"placeholder": "Salary Computation", "class": "form-control"}),
        }