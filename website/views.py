from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  AttendanceForm, TimeOutForm, EditAttendanceFormAdmin
from .models import Attendance
from django.urls import reverse
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
# Create your views here.

# landing page
def home(request):
    return render(request, 'home.html',)

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
            messages.success(request, "You have been logged in!")
            return redirect(reverse('welcome', kwargs={'username': username}))
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def welcome_view(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'welcome.html', {'username': username})
    else:
        logout(request)
        messages.success(request, "You must be logged it to access the page")
        return redirect('home')  
    
# logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


# attendance_list admin
def attendance_list(request, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.user.is_employee:
            employeeID = request.user.id
            attendances = Attendance.objects.filter(employeeID=employeeID)
        else:
            attendances = Attendance.objects.all()
            
        for attendance in attendances:
            computed_salary = calculate_computed_salary(attendance.time_in, attendance.time_out, attendance.salary)
            attendance.computed_salary = computed_salary
        return render(request, 'attendanceList.html',{'attendances': attendances, 'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')






# create time in (for employees) (add autofill) (add security)  
def time_In(request, username):
    if request.user.is_authenticated and request.user.username == username:
        today_records = Attendance.objects.filter(date=timezone.now().date(), employeeID=request.user.id)
        if today_records.exists():
            messages.error(request, "You have already timed in for today.")
            return redirect('home')

        if request.method == "POST":
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.user = request.user
                attendance.save()
                messages.success(request, "Record Added")
                return redirect('home')
        else:
            initial_data = {
                'employeeID': request.user.id,
                'employee_Name': f"{request.user.first_name} {request.user.last_name}",
            }
            form = AttendanceForm(initial=initial_data)
        return render(request, 'timeIn.html', {'form': form})
    else:
        return redirect('attendanceList', username=username)
    
    # time out
def time_Out(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        current_record = Attendance.objects.get(id=pk)
        truncated_time_in = truncate_to_minutes(current_record.time_in)
        truncated_time_out = truncate_to_minutes(current_record.time_out)
        if truncated_time_in == truncated_time_out:
            form = TimeOutForm(request.POST or None, instance=current_record)
            
            computed_salary = None
            if current_record.time_in and current_record.salary:
                computed_salary = calculate_computed_salary_timeout(current_record.time_in, current_record.salary)
            
            if computed_salary is not None:
                form.initial['salary_computation'] = computed_salary
            
            if form.is_valid():
                form.instance.on_duty = False
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('attendanceList', {'username': username})
            return render(request, 'timeOut.html', {'form': form, 'computed_salary': computed_salary})
        else:
            messages.warning(request, "Record already timed out.")
            return redirect('attendanceList', {'username': username})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

 # admin attendance individual record
def attendance_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        attendance_record = Attendance.objects.get(id=pk)
        computed_salary = calculate_computed_salary(attendance_record.time_in, attendance_record.time_out, attendance_record.salary)
        return render(request, 'attendanceRecord.html', {'attendance_record': attendance_record, 'computed_salary': computed_salary, 'username': username})
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



def AdminUpdateAttendaceRecord(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.user.is_superuser:
            current_record = Attendance.objects.get(id=pk)
            form = EditAttendanceFormAdmin(request.POST or None, instance=current_record)
            if request.method == "POST":
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record has been updated successfully!")
                    return redirect('attendanceList')
            return render(request, 'AdminEditAttendance.html', {'form': form, 'username': username})
        else:
            messages.error(request, "You must be an admin to edit this.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')

    

