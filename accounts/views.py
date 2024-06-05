from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from .models import User
from .forms import EmployeeSignUpForm, SupervisorSignUpForm
from django.views.generic import CreateView
from django.urls import reverse

def home(request):
    return render(request, 'home.html',)

class supervisor_register(CreateView):
    model = User
    form_class = SupervisorSignUpForm
    template_name = 'supervisor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'employee_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
    
