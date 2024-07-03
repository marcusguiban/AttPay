from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  AttendanceForm, TimeOutForm, EditAttendanceFormAdmin, AttendanceFormAdmin, PayslipForm, ScheduleForm
from .models import Attendance, PaySlip, Schedule
from django.urls import reverse
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from datetime import timedelta
from accounts.models import Employee, Supervisor
import threading
import time
# Create your views here.

# landing page


def notfound(request):
    return render(request, '404.html',)
# login page (admin)
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_employee:
                messages.success(request, "You have been logged in!")
                return redirect(reverse('home'))
            else:
                messages.success(request, "You have been logged in!")
                return redirect(reverse('home'))
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
# logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')



def attendance_list(request, username):
    form = AttendanceFormAdmin(request.POST or None)
    if request.user.is_authenticated and request.user.username == username:
        filter_date = request.GET.get('date')
        filter_employee_id = request.GET.get('employee_id')
        filter_paid = request.GET.get('paid')  # Get the paid filter parameter

        if request.user.is_employee:
            employeeID = request.user.id
            attendances = Attendance.objects.filter(employeeID=employeeID)
        else:
            attendances = Attendance.objects.all()

        if filter_date:
            attendances = attendances.filter(date=filter_date)
        if filter_employee_id:
            attendances = attendances.filter(employeeID=filter_employee_id)
        if filter_paid:
            if filter_paid.lower() == 'true':
                attendances = attendances.filter(paid=True)
            elif filter_paid.lower() == 'false':
                attendances = attendances.filter(paid=False)

        attendances = attendances.order_by('-date')

        if request.user.is_superuser:
            if request.method == "POST" and form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('attendanceList', username=username)
            return render(request, 'attendanceList.html', {
                'form': form,
                'attendances': attendances,
                'username': username,
                'filter_date': filter_date,
                'filter_employee_id': filter_employee_id,
                'filter_paid': filter_paid  # Pass filter_paid to template context
            })

        return render(request, 'attendanceList.html', {
            'attendances': attendances,
            'username': username,
            'filter_date': filter_date,
            'filter_employee_id': filter_employee_id,
            'filter_paid': filter_paid  # Pass filter_paid to template context
        })
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')

def home(request):   
    return render(request, 'home.html')

def set_off_duty(user_record):
    time.sleep(12 * 3600)  # Wait for 12 hours
    user_record.on_duty = False
    user_record.save()


def time_In(request, username):
    if request.user.is_authenticated and (request.user.username == username or request.user.is_superuser):
        # Check if the user is already on duty
        if request.user.is_employee:
            user_record = Employee.objects.get(user=request.user)
        elif request.user.is_supervisor:
            user_record = Supervisor.objects.get(user=request.user)
        else:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('attendanceList', username=username)
        
        if user_record.on_duty:
            messages.error(request, "You are already on duty.")
            return redirect('attendanceList', username=username)

        ip_address = get_client_ip(request)
        if ip_address == "192.168.68.121":
            duty_location = "Test Location"
        elif ip_address == "127.0.0.1":
            duty_location = "Local Host"
        else:
            duty_location = "Location not recognized"
        
        if request.method == "POST":
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.user = request.user
                attendance.date = datetime.now().date()
                attendance.time_in = datetime.now().time()
                attendance.time_out = (datetime.now() + timedelta(hours=4)).time()
                attendance.duty_location = duty_location  # Set the duty location based on IP address
                attendance.save()
                
                # Update the on_duty status for the user
                user_record.on_duty = True
                user_record.save()

                # Start a background thread to set on_duty to False after 12 hours
                threading.Thread(target=set_off_duty, args=(user_record,)).start()

                messages.success(request, "Record Added")
                return redirect('attendanceList', username=username)
        else:
            initial_data = {
                'employeeID': request.user.id,
                'employee_Name': f"{request.user.first_name} {request.user.last_name}",
                'duty_location': duty_location, 
                'date': datetime.now().date(),
                'time_in': datetime.now().time(),
                'time_out': (datetime.now() + timedelta(hours=4)).time(),  # Initial value for time_out
            }
            form = AttendanceForm(initial=initial_data)
        
        return render(request, 'timeIn.html', {'form': form})
    else:
        return redirect('attendanceList', username=username)
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def time_Out(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            if request.user.is_employee:
                current_record = Employee.objects.get(user=request.user)
            elif request.user.is_supervisor:
                current_record = Supervisor.objects.get(user=request.user)
            else:
                messages.error(request, "You are not authorized to perform this action.")
                return redirect('attendanceList', username=username)
            
            # Check if the user is on duty
            if not current_record.on_duty:
                messages.warning(request, "You are not currently on duty.")
                return redirect('attendanceList', username=username)

            attendance_record = Attendance.objects.get(id=pk, employeeID=request.user.id)
            form = TimeOutForm(request.POST or None, instance=attendance_record)
            
            computed_salary = None
            working_hours = None
            if attendance_record.time_in and attendance_record.time_out:
                # Compute salary
                computed_salary = calculate_computed_salary_timeout(attendance_record.time_in, attendance_record.salary)
                
                # Compute work hours
                current_time = datetime.now().time()
                time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), attendance_record.time_in)
                hours = int(time_difference.total_seconds() // 3600)
                minutes = int((time_difference.total_seconds() % 3600) // 60)
                working_hours = f"{hours} hours {minutes} minutes"
            
            if computed_salary is not None:
                form.initial['salary_computation'] = computed_salary
            if working_hours is not None:
                form.initial['working_hours'] = working_hours
                
            # Set initial value for time_out to current time
            form.initial['time_out'] = datetime.now().time()
            
            if form.is_valid():
                form.instance.on_duty = False
                form.save()

                # Update the on_duty status for the user
                current_record.on_duty = False
                current_record.save()

                messages.success(request, "Record Has Been Updated!")
                return redirect('attendanceList', username=username)
            
            return render(request, 'timeOut.html', {'form': form, 'computed_salary': computed_salary, 'working_hours': working_hours})
        
        except Employee.DoesNotExist:
            messages.error(request, "Employee record does not exist.")
            return redirect('attendanceList', username=username)
        
        except Supervisor.DoesNotExist:
            messages.error(request, "Supervisor record does not exist.")
            return redirect('attendanceList', username=username)
        except Attendance.DoesNotExist:
            messages.error(request, "Attendance record does not exist.")
            return redirect('attendanceList', username=username)
    
    else:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('attendanceList', username=username)

 # admin attendance individual record
def attendance_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        attendance_record = Attendance.objects.get(id=pk)
        
        time_difference = datetime.combine(datetime.today(), attendance_record.time_out) - datetime.combine(datetime.today(), attendance_record.time_in)
        hours = int(time_difference.total_seconds() / 3600)
        minutes = int((time_difference.total_seconds() % 3600) / 60)
        formatted_time_difference = f"{hours} hours {minutes} minutes"  # Formatting time_difference
        
        computed_salary = calculate_computed_salary(attendance_record.time_in, attendance_record.time_out, attendance_record.salary)
        
        return render(request, 'attendanceRecord.html', {'attendance_record': attendance_record, 'computed_salary': computed_salary, 'formatted_time_difference': formatted_time_difference, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')


    # deletion of record
def delete_record(request, pk,username):
    if request.user.is_authenticated and request.user.username == username:
        delete_it = Attendance.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('attendanceList',  username=username)
    else:
        messages.success(request, "You Must be logged in to delete this record")
        return redirect('attendanceList', username=username)
# computations
def AdminUpdateAttendanceRecord(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.user.is_superuser:
            current_record = get_object_or_404(Attendance, pk=pk)
            if request.method == "POST":
                form = EditAttendanceFormAdmin(request.POST, instance=current_record)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record has been updated successfully!")
                    return redirect('home')
            else:
                # Set initial values for time_in and time_out fields
                form = EditAttendanceFormAdmin(instance=current_record, initial={'time_in': current_record.time_in, 'time_out': current_record.time_out})
            return render(request, 'AdminEditAttendance.html', {'form': form, 'username': username})
        else:
            messages.error(request, "You must be an admin to edit this.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')
    
def create_payslip(request, username):
    form = PayslipForm(request.POST or None)
    if request.user.is_authenticated and request.user.username == username:
            if request.method == "POST":
                if form.is_valid():
                    add_playslip = form.save()
                    messages.success(request, "Record Added")
                    return redirect('home')
            return render(request, 'create_payslip.html',{'form':form,  'username': username})
    else:
        messages.success(request, "You Must be logged in to add record")
        return redirect('home')
    


def payslip_list(request, username):
    paySlips = PaySlip.objects.all()
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'payslip_list.html',{'paySlips': paySlips, 'username': username})
    else:
        messages.success(request, "You Must be logged in to view the list")
        return redirect('home')


def payslip_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        payslip_record = PaySlip.objects.get(id=pk)
        return render(request, 'payslip_record.html', {'payslip_record': payslip_record, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')



def delete_payslip(request, pk,username):
    if request.user.is_authenticated and request.user.username == username:
        delete_it = PaySlip.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('payslip_list',  username=username)
    else:
        messages.success(request, "You Must be logged in to delete this record")
        return redirect('home')

def update_payslip(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        payslip_record = PaySlip.objects.get(id=pk)
        form = PayslipForm(request.POST or None, instance=payslip_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('payslip_list',  username=username)
        return render(request, 'payslip_update.html', {'form':form, 'username': username})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def schedule_create(request, username):
    form = ScheduleForm(request.POST or None)
    if request.user.is_authenticated and request.user.username == username:
            if request.method == "POST":
                if form.is_valid():
                    add_playslip = form.save()
                    messages.success(request, "Record Added")
                    return redirect('home')
            return render(request, 'schedule_create.html',{'form':form,  'username': username})
    else:
        messages.success(request, "You Must be logged in to add record")
        return redirect('home')


def schedule_list(request, username):
    schedules = Schedule.objects.all()
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'schedule_list.html',{'schedules': schedules, 'username': username})
    else:
        messages.success(request, "You Must be logged in to view the list")
        return redirect('home')


def schedule_update(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        schedule_record = Schedule.objects.get(id=pk)
        form = ScheduleForm(request.POST or None, instance=schedule_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule Has Been Updated!")
            return redirect('schedule_list',  username=username)
        return render(request, 'schedule_update.html', {'form':form, 'username': username})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def schedule_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        schedule_record = Schedule.objects.get(id=pk)
        return render(request, 'schedule_record.html', {'schedule_record': schedule_record, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')

def schedule_delete(request, pk,username):
    if request.user.is_authenticated and request.user.username == username:
        delete_it = Schedule.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Schedule Deleted Successfully")
        return redirect('schedule_list',  username=username)
    else:
        messages.success(request, "You Must be logged in to delete this record")
        return redirect('home')






def truncate_to_minutes(time):
    return time.replace(second=0, microsecond=0)

def calculate_computed_salary(time_in, time_out, salary):
    time_difference = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), time_in)
    hours_difference = time_difference.total_seconds() / 3600
    salary_decimal = Decimal(salary)
    computed_salary = (salary_decimal / Decimal(9)) * Decimal(hours_difference)
    computed_salary = computed_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return computed_salary

def calculate_computed_salary_timeout(time_in, salary):
    current_time = datetime.now().time()
    time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), time_in)
    hours_difference = time_difference.total_seconds() / 3600
    salary_decimal = Decimal(salary)
    computed_salary = (salary_decimal / Decimal(9)) * Decimal(hours_difference)
    computed_salary = computed_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return computed_salary





    

