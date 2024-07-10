from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import User, Employee, Supervisor
from .forms import EmployeeSignUpForm, SupervisorSignUpForm, EmployeeUpdateForm, SupervisorUpdateForm
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse
from website.models import Attendance, Schedule, PaySlip
from django.views import View
from django.utils.dateparse import parse_date
from django.db.models import Sum
from website.forms import PayslipForm
from datetime import datetime
from django.db import transaction
def home(request):
    return render(request, 'home.html',)

class supervisor_register(CreateView):
    model = User
    form_class = SupervisorSignUpForm
    template_name = 'supervisor_register.html'

    def form_valid(self, form ):
        form.save() 
        messages.success(self.request, "Registration successful! You can now log in.")
        return redirect('/')
    def get_success_url(self):
        return reverse('supervisor_list', kwargs={'username': self.request.user.username})

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'employee_register.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Registration successful! You can now log in.")
        return redirect('/')
    def get_success_url(self):
        return reverse('employee_list', kwargs={'username': self.request.user.username})
    
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
     
def supervisor_update(request, pk, username):
	if request.user.is_authenticated and request.user.username == username:
		current_record = Supervisor.objects.get(user_id=pk)
		form = SupervisorUpdateForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'supervisor_update.html', {'form':form, 'username': username})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

def employee_list(request, username):
    if request.user.is_authenticated and request.user.username == username:
        employees = Employee.objects.all()
        employees_on_duty = employees.filter(on_duty=True)
        employees_not_on_duty = employees.filter(on_duty=False)
        return render(request, 'employee_list.html', {'employees': employees, 'employees_on_duty': employees_on_duty, 'employees_not_on_duty': employees_not_on_duty, 'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')

def supervisor_list(request, username):
    if request.user.is_authenticated and request.user.username == username:
        supervisors = Supervisor.objects.all()
        supervisors_on_duty = supervisors.filter(on_duty=True)
        supervisors_not_on_duty = supervisors.filter(on_duty=False)
        return render(request, 'supervisor_list.html', {'supervisors': supervisors, 'supervisors_on_duty': supervisors_on_duty, 'supervisors_not_on_duty': supervisors_not_on_duty,  'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')


def employee_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            employee_record = Employee.objects.get(user_id=pk)
        except Employee.DoesNotExist:
            messages.error(request, "Employee record does not exist")
            return redirect('home')

        if request.user.is_employee and employee_record.user_id != request.user.id:
            messages.error(request, "You are not authorized to view this employee's record")
            return redirect('home')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        attendances = Attendance.objects.filter(employeeID=pk, paid=False)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__range=(start_date, end_date))
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        elif start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__gte=start_date)
            except ValueError:
                messages.error(request, "Invalid start date format. Please use YYYY-MM-DD.")
        elif end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__lte=end_date)
            except ValueError:
                messages.error(request, "Invalid end date format. Please use YYYY-MM-DD.")

        total_salary_computation = attendances.aggregate(total=Sum('salary_computation'))
        total_salary = total_salary_computation['total'] if total_salary_computation['total'] else 0

        schedules = Schedule.objects.filter(employeeID=pk)
        payslips = PaySlip.objects.filter(employeeID=pk)

        initial_data = {
            'employeeID': pk,
            'employee_name': f"{employee_record.user.first_name} {employee_record.user.last_name}",
            'date_start': start_date,
            'date_end': end_date,
            'total_salary': total_salary
        }

        form = PayslipForm(request.POST or None, initial=initial_data)

        if request.method == "POST":
            if form.is_valid():
                payslip_instance = form.save(commit=False)
                payslip_instance.save()

                # Update attendance records to paid=True
                with transaction.atomic():
                    for attendance in attendances:
                        attendance.paid = True
                        attendance.save()

                messages.success(request, "Payslip Created and Attendance Records Updated")
                return redirect('home')

        return render(request, 'employee_record.html', {
            'employee_record': employee_record,
            'attendances': attendances,
            'schedules': schedules,
            'payslips': payslips,
            'username': username,
            'total_salary_computation': {
                'start_date': start_date,
                'end_date': end_date,
                'total': total_salary,
            },
            'form': form
        })
    else:
        messages.error(request, "You must be logged in to view that page")
        return redirect('home')

def supervisor_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            supervisor_record = Supervisor.objects.get(user_id=pk)
        except Supervisor.DoesNotExist:
            messages.error(request, "Supervisor record does not exist")
            return redirect('home')

        if request.user.is_supervisor and supervisor_record.user_id != request.user.id:
            messages.error(request, "You are not authorized to view this supervisor's record")
            return redirect('home')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter attendances based on employee ID and paid status
        attendances = Attendance.objects.filter(employeeID=pk, paid=False)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__range=(start_date, end_date))
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        elif start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__gte=start_date)
            except ValueError:
                messages.error(request, "Invalid start date format. Please use YYYY-MM-DD.")
        elif end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                attendances = attendances.filter(date__lte=end_date)
            except ValueError:
                messages.error(request, "Invalid end date format. Please use YYYY-MM-DD.")

        total_salary_computation = attendances.aggregate(total=Sum('salary_computation'))
        total_salary = total_salary_computation['total'] if total_salary_computation['total'] else 0

        schedules = Schedule.objects.filter(employeeID=pk)
        payslips = PaySlip.objects.filter(employeeID=pk)

        initial_data = {
            'employeeID': pk,
            'employee_name': f"{supervisor_record.user.first_name} {supervisor_record.user.last_name}",
            'date_start': start_date,
            'date_end': end_date,
            'total_salary': total_salary
        }

        form = PayslipForm(request.POST or None, initial=initial_data)

        if request.method == "POST":
            if form.is_valid():
                payslip_instance = form.save(commit=False)
                payslip_instance.save()

                # Update attendance records to paid=True
                with transaction.atomic():
                    for attendance in attendances:
                        attendance.paid = True
                        attendance.save()

                messages.success(request, "Payslip Created and Attendance Records Updated")
                return redirect('home')

        return render(request, 'supervisor_record.html', {
            'supervisor_record': supervisor_record,
            'attendances': attendances,
            'schedules': schedules,
            'payslips': payslips,
            'username': username,
            'total_salary_computation': {
                'start_date': start_date,
                'end_date': end_date,
                'total': total_salary,
            },
            'form': form
        })
    else:
        messages.error(request, "You must be logged in to view that page")
        return redirect('home')

def delete_employee(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            employee = Employee.objects.get(user_id=pk)
            user = employee.user  
            employee.delete()
            user.delete()
            messages.success(request, "Employee Record Deleted Successfully")
        except Employee.DoesNotExist:
            messages.error(request, "Employee record does not exist")
    else:
        messages.error(request, "You must be logged in to delete this record")
    return redirect('employee_list', username=username)

def delete_supervisor(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            supervisor = Supervisor.objects.get(user_id=pk)
            user = supervisor.user 
            supervisor.delete()
            user.delete()
            messages.success(request, "Supervisor Record Deleted Successfully")
        except Supervisor.DoesNotExist:
            messages.error(request, "Supervisor record does not exist")
    else:
        messages.error(request, "You must be logged in to delete this record")
    return redirect('supervisor_list', username=username)