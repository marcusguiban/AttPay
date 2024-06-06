from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import User, Employee, Supervisor
from .forms import EmployeeSignUpForm, SupervisorSignUpForm, EmployeeUpdateForm, SupervisorUpdateForm
from django.views.generic import CreateView
from django.contrib import messages
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
    
    def get_success_url(self):
        return reverse('supervisor_list', kwargs={'username': self.request.user.username})

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'employee_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
    def get_success_url(self):
        return reverse('employee_list', kwargs={'username': self.request.user.username})

def employee_list(request, username):
    if request.user.is_authenticated and request.user.username == username:
        employees = Employee.objects.all()
        return render(request, 'employee_list.html', {'employees': employees,'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')

def supervisor_list(request, username):
    if request.user.is_authenticated and request.user.username == username:
        supervisors = Supervisor.objects.all()
        return render(request, 'supervisor_list.html', {'supervisors': supervisors, 'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')



def employee_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        employee_record = Employee.objects.get(user_id=pk)
        return render(request, 'employee_record.html', {'employee_record': employee_record, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    
def supervisor_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        supervisor_record = Supervisor.objects.get(user_id=pk)
        return render(request, 'supervisor_record.html', {'supervisor_record': supervisor_record, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')

def employee_update(request, pk, username):
	if request.user.is_authenticated and request.user.username == username:
		current_record = Employee.objects.get(user_id=pk)
		form = EmployeeUpdateForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'employee_update.html', {'form':form, 'username': username})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
