from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Supervisor,Employee
from django.forms import ModelForm

class SupervisorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    occupation = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supervisor = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        supervisor = Supervisor.objects.create(user=user)
        supervisor.phone_number=self.cleaned_data.get('phone_number')
        supervisor.location=self.cleaned_data.get('location')
        supervisor.occupation=self.cleaned_data.get('occupation')
        supervisor.save()
        return user

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    occupation = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user)
        employee.phone_number=self.cleaned_data.get('phone_number')
        employee.location=self.cleaned_data.get('location')
        employee.occupation=self.cleaned_data.get('occupation')
        employee.save()
        return user
class SupervisorUpdateForm(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    on_duty = forms.BooleanField(required=False)
    class Meta:
        model = Supervisor
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'occupation', 'on_duty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for first_name, last_name, and email fields from associated User instance
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['on_duty'].initial = self.instance.user.on_duty

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Update associated User instance with the updated first_name, last_name, and email fields
            user = instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.on_duty = self.cleaned_data['on_duty']
            user.save()
        return instance
    



class EmployeeUpdateForm(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'occupation', 'on_duty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for first_name, last_name, and email fields from associated User instance
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Update associated User instance with the updated first_name, last_name, and email fields
            user = instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.on_duty = self.cleaned_data['on_duty']
            user.save()
        return instance