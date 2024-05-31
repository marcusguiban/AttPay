from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Attendance


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-controll', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,  widget=forms.TextInput(attrs={'class': 'form-controll', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="",  max_length=100, widget=forms.TextInput(attrs={'class': 'form-controll', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class AttendanceForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Duty Location", "class":"form-control"}), label="")
    status = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Timed in", "class":"form-control"}), label="")

    class Meta:
        model = Attendance
        exclude = ("user", "salary", "salary_computation")

class TimeOutForm(forms.ModelForm):

    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control", "readonly": "readonly"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control", "readonly": "readonly"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control", "readonly": "readonly"}), label="")
    duty_location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Duty Location", "class":"form-control", "readonly": "readonly"}), label="")
    status = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Timed in", "class":"form-control"}), label="")

    class Meta:
        model = Attendance
        exclude = ("user",)